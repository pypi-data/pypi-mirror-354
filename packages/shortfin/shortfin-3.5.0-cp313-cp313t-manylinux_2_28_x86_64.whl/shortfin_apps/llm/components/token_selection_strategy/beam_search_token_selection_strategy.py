# Copyright 2025 Advanced Micro Devices, Inc.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import logging
import numpy as np

from typing import List

from .base_token_selection_strategy import (
    BaseTokenSelectionStrategy,
    TokenSelectionStrategyConfig,
)
from .beam_group import BeamGroup, Beam
from .config import LogitsNormalization
from ..messages import LlmInferenceExecRequest, InferencePhase


logger = logging.getLogger(__name__)


TOP_P_DEFAULT_SELECTION = 32


class BeamSearchBeam(Beam):
    def _convert_results_to_log_probs(
        self,
        probs: np.array,
    ):
        log_probs = self.convert_logits_normalization(
            LogitsNormalization.SOFTMAX,
            LogitsNormalization.LOG_SOFTMAX,
            probs,
        )

        return log_probs.tolist()

    def sample_logits(self, k: int):
        """Obtain tokens and log_probs from beam_search or beam_search with sampling.

        Args:
            k (int): Number of max elements to return.

        Returns:
            Tuple[List[int], List[float]]: Tuple containing (top_tokens, top_values)
        """
        exec_req = self.exec_req
        decode_config = self.decode_config
        top_k = decode_config.top_k
        top_p = decode_config.top_p

        logits = np.array(exec_req.result_logits)
        indices = exec_req.result_indices
        indices = np.array(indices) if indices is not None else None

        if (top_k, top_p) == (None, None):
            tokens, probs = self.sampler.select_top_k(logits, indices, -k)

            if self.decode_config.logits_normalization == LogitsNormalization.NONE:
                probs = self.apply_temperature(probs)

            log_probs = self.convert_logits_normalization(
                self.decode_config.logits_normalization,
                LogitsNormalization.LOG_SOFTMAX,
                probs,
            ).tolist()

            return tokens, log_probs

        if top_k is not None:
            # Sample from `top_k` tokens
            tokens, probs = self._sample_logits_top_k(
                logits,
                indices,
                top_k,
                num_selections=top_k,
            )

        if top_p is not None:
            if top_k is None:
                top_p_selection = min(logits.shape[-1], TOP_P_DEFAULT_SELECTION)
                tokens, values = self.sampler.select_top_k(
                    logits, indices, -top_p_selection
                )
                probs = self._to_softmax(
                    values,
                    self.decode_config.logits_normalization,
                )

                if indices is None:
                    sorted_order = np.argsort(probs)[::-1]
                    tokens = tokens[sorted_order]
                    probs = probs[sorted_order]

            tokens, probs = self._sample_logits_top_p(
                tokens, probs, top_p, k, return_probs=True
            )

        log_probs = self._convert_results_to_log_probs(
            probs,
        )

        return tokens, log_probs

    def update_score(self, log_prob: float):
        """Increment the cumulative_log_prob of the beam.

        Args:
            log_prob (float): Log probability of the token.
        """
        self.score += log_prob

    def update_exec_req(self):
        """Add a selected token to a request after a decode loop."""
        self.exec_req.input_token_ids.append(self.last_token)
        self.exec_req.start_position += 1

    def normalize_score(self, min_log_prob: float):
        """Track the accumulated_normalization for a given beam.

        Args:
            min_log_prob (float): Minimum log probability of the selected tokens.
        """
        self.accumulated_normalization += abs(min_log_prob)

    def update_final_score(self):
        """Calculate the final score of a beam, with a brevity penalty."""
        exec_req = self.exec_req
        self.score = (self.score - self.accumulated_normalization) / (
            len(exec_req.input_token_ids) - exec_req.prompt_length
        )


class BeamSearchTokenSelectionStrategy(BaseTokenSelectionStrategy):
    min_log_prob: float = 0.0

    def select_top_k(
        self,
        active_beams: List[BeamSearchBeam],
        completed_beams: List[BeamSearchBeam],
    ) -> List[BeamSearchBeam]:
        """Handle the selection of the `top_k` beams within a decode step.

        Args:
            active_beams (List[BeamSearchBeam]): Beams that are still active.
            completed_beams (Set[BeamSearchBeam]): Beams that have been completed.

        Returns:
            List[BeamSearchBeam]: The `top_k` selections, containing necessary info for `beam_group` to handle choosing and processing beams.
        """
        config = self.token_selection_strategy_config
        k = config.decode_config.num_beams - len(completed_beams)

        global_min_log_prob = 0.0

        top_score = None
        top_beam = None
        selections: List[BeamSearchBeam] = []
        for beam in active_beams:
            min_log_prob = 0.0
            top_tokens, top_values = beam.sample_logits(k)
            for token, value in zip(top_tokens, top_values):
                if value < min_log_prob:
                    min_log_prob = value

                new_beam = BeamSearchBeam(
                    exec_req=beam.exec_req,
                    score=beam.score,
                    accumulated_normalization=beam.accumulated_normalization,
                    last_token=token,
                    decode_config=config.decode_config,
                )
                new_beam.update_score(value)
                selections.append(new_beam)

                if top_score is None or new_beam.score > top_score:
                    top_score = new_beam.score
                    top_beam = new_beam

            if min_log_prob < global_min_log_prob:
                global_min_log_prob = min_log_prob

        if len(selections) < config.decode_config.num_beams:
            beams_to_add = config.decode_config.num_beams - len(selections)
            for _ in range(beams_to_add):
                new_beam = BeamSearchBeam(
                    exec_req=top_beam.exec_req,
                    score=top_beam.score,
                    accumulated_normalization=top_beam.accumulated_normalization,
                    last_token=top_beam.last_token,
                    decode_config=config.decode_config,
                )
                selections.append(new_beam)

        sorted_selections = sorted(
            selections, key=lambda beam: beam.score, reverse=True
        )[:k]
        for beam in sorted_selections:
            beam.normalize_score(global_min_log_prob)
        return sorted_selections

    def _find_top_beam(
        self,
        active_beams: List[BeamSearchBeam],
        completed_beams: List[BeamSearchBeam],
    ) -> BeamSearchBeam:
        """Find the highest scoring beam, post generation.

        Args:
            active_beams (List[BeamSearchBeam]): Beams that are still actively generating.
            completed_beams (List[BeamSearchBeam]): Beams that have completed.

        Returns:
            BeamSearchBeam: Highest scoring beam.
        """
        beams = list(completed_beams) if completed_beams else active_beams
        for beam in beams:
            beam.update_final_score()
        return max(beams, key=lambda beam: beam.score)

    async def decode(
        self,
        exec_req: LlmInferenceExecRequest,
    ):
        """Orchestrate decode loop for `beam_search` selection strategy.

        Args:
            exec_req (LlmInferenceExecRequest): Initial inference request, post prefill.
        """
        self._log_sampling_method()
        config = self.token_selection_strategy_config

        beam_group = BeamGroup(
            config.eos_token_id,
            config.decode_config.num_beams,
            [BeamSearchBeam(exec_req, decode_config=config.decode_config)],
            self.select_top_k,
        )

        reservations = beam_group.active_beam_count
        config.decode_begin_callback(rid=exec_req.orig_instance_id, count=reservations)
        for _ in range(config.decode_config.max_completion_tokens):
            if exec_req.status_tracker.is_disconnected():
                break
            if not beam_group.active_beams:
                break

            active_beam_count = len(beam_group.active_beams)
            if reservations > active_beam_count:
                release_amount = reservations - active_beam_count

                config.decode_end_callback(
                    rid=exec_req.orig_instance_id, count=release_amount
                )
                reservations = active_beam_count

            if reservations < active_beam_count:
                acquire_amount = active_beam_count - reservations
                config.decode_begin_callback(
                    rid=exec_req.orig_instance_id, count=acquire_amount
                )
                reservations = active_beam_count

            for beam in beam_group.active_beams:
                req = beam.exec_req
                req.reset(InferencePhase.DECODE)
                config.decode_callback(req)
            await beam_group.wait()
            beam_group.process_beams()

        config.decode_end_callback(rid=exec_req.orig_instance_id, count=reservations)
        beam_group.clean_up()
        self.get_results(beam_group)

    def get_results(self, beam_group: BeamGroup):
        """Get the results of a `beam_search` request, post generation.

        Args:
            beam_group (BeamGroup): Helper instance containing our beams.
        """
        config = self.token_selection_strategy_config
        results = [
            beam.exec_req.input_token_ids[beam.exec_req.prompt_length :]
            for beam in beam_group.completed_beams
        ]
        if len(results) < beam_group.num_beams:
            for beam in beam_group.active_beams:
                beam.update_final_score()

            active_beams = sorted(
                [beam for beam in beam_group.active_beams],
                key=lambda beam: beam.score,
                reverse=True,
            )
            for i in range(beam_group.num_beams - len(results)):
                beam = active_beams[i]
                results.append(
                    beam.exec_req.input_token_ids[beam.exec_req.prompt_length :]
                )
        config.results_callback(results)
