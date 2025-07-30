import time
import logging
from queue import Empty, Queue
from typing import TYPE_CHECKING, List
from typing_extensions import TypeAlias

from scale_gp_beta import SGPClient
from scale_gp_beta._exceptions import APIError
from scale_gp_beta.types.span_upsert_batch_params import Item as SpanCreateRequest

from .exceptions import ParamsCreationError

if TYPE_CHECKING:
    from .tracing import Span

INITIAL_BACKOFF = 0.4
MAX_BACKOFF = 20

log: logging.Logger = logging.getLogger(__name__)

SpanRequestBatch: TypeAlias = List[SpanCreateRequest]


class TraceExporter:
    def __init__(
        self,
        max_batch_size: int,
        max_retries: int,
        backoff: float = INITIAL_BACKOFF,
        max_backoff: float = MAX_BACKOFF,
    ):
        self.max_batch_size = max_batch_size
        self.max_retries = max_retries
        self.backoff = backoff
        self.max_backoff = max_backoff

    def export(self, client: SGPClient, queue: "Queue[Span]") -> None:
        # export finished spans, note we do a check to ensure spans are finished in spans.py #to_request_params()
        # this is also thread safe, two threads can call this method with the same queue at once
        # the ordering of the requests might be randomly split between the two threads, but they should all be picked up
        batches: list[SpanRequestBatch] = self._create_batches(queue)

        log.info(f"Exporting {len(batches)} span batches")

        for batch in batches:
            self._export_batch(batch, client)

    def _export_batch(self, batch: SpanRequestBatch, client: SGPClient) -> None:
        attempts_remaining = self.max_retries
        backoff_delay = self.backoff
        while attempts_remaining > 0:
            attempts_remaining -= 1
            try:
                client.spans.upsert_batch(items=batch)
                return
            except APIError as e:
                log.warning(
                    f"API error occurred while exporting batch: {e.message}, attempts remaining: {attempts_remaining}"
                )
                if attempts_remaining == 0:
                    continue
                time.sleep(backoff_delay)
                backoff_delay = min(backoff_delay * 2, self.max_backoff)

        log.error(f"Failed to export span batch after {self.max_retries} attempts, dropping...")

    def _create_batches(self, queue: "Queue[Span]") -> "list[SpanRequestBatch]":
        """Drain the queue and return a list of batches"""
        batches: list[SpanRequestBatch] = []

        while True:
            span_batch: SpanRequestBatch = []

            while len(span_batch) < self.max_batch_size and queue.qsize() > 0:
                try:
                    span: "Span" = queue.get_nowait()
                    span_request = span.to_request_params()
                    span_batch.append(span_request)
                except Empty:
                    break
                except ParamsCreationError as e:
                    log.warning(f"ParamsCreationError: {e}\ndropping...")

            if not span_batch:
                break
            batches.append(span_batch)

        return batches
