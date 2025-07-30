import logging
from typing import Any, Dict, Union, Optional

from .span import Span, BaseSpan, NoOpSpan
from .util import is_disabled
from .scope import Scope
from .trace import Trace, BaseTrace, NoOpTrace
from .trace_queue_manager import tracing_queue_manager

log: logging.Logger = logging.getLogger(__name__)


def current_span() -> Optional[BaseSpan]:
    """Retrieves the currently active span from the execution context.

    This function relies on `contextvars` to manage the active span in
    a context-local manner, making it safe for concurrent execution
    environments (e.g., threads, asyncio tasks).

    Returns:
        Optional[BaseSpan]: The current BaseSpan instance if one is active,
                            otherwise None. This could be a 'Span' or 'NoOpSpan'.
    """
    return Scope.get_current_span()


def current_trace() -> Optional[BaseTrace]:
    """Retrieves the currently active trace from the execution context.

    Similarly, to `current_span()`, this uses `contextvars` for context-local
    trace management.

    Returns:
        Optional[BaseTrace]: The current BaseTrace instance if one is active,
                             otherwise None. This could be a 'Trace' or 'NoOpTrace'.
    """
    return Scope.get_current_trace()


def flush_queue() -> None:
    """
    Blocking flush of all requests in the queue.

    Useful for distributed applications to ensure spans have been committed before continuing.
    :return:
    """
    queue_manager = tracing_queue_manager()
    queue_manager.flush_queue()


def create_trace(
        name: str,
        trace_id: Optional[str] = None,
        root_span_id: Optional[str] = None,
        metadata: Optional[Dict[str, Optional[str]]] = None,
) -> BaseTrace:
    """Creates a new trace and root span instance.

    A trace represents a single, logical operation or workflow. It groups multiple
    spans together. If tracing is disabled (via the 'DISABLE_SCALE_TRACING'
    environment variable), a `NoOpTrace` instance is returned which performs no
    actual tracing operations.

    When a trace is started (e.g., by using it as a context manager or calling its
    `start()` method), it becomes the `current_trace()` in the active scope.
    Similarly, the root span instance becomes the `current_span()` in the active
    scope.

    Args:
        name: The name of the trace.
        trace_id (Optional[str]): An optional, user-defined ID for the trace.
                                  If None, a unique trace ID will be generated.
        root_span_id (Optional[str]): An optional, user-defined ID for the root span.
        metadata (Optional[Dict[str, Optional[str]]]): An optional, user-defined metadata.

    Returns:
        BaseTrace: A `Trace` instance if tracing is enabled, or a `NoOpTrace`
                   instance if tracing is disabled.
    """
    if is_disabled():
        log.debug(f"Tracing is disabled. Not creating a new trace.")
        return NoOpTrace(name=name, trace_id=trace_id, root_span_id=root_span_id, metadata=metadata)

    active_trace = current_trace()
    if active_trace is not None:
        log.warning(f"Trace with id {active_trace.trace_id} is already active. Creating a new trace anyways.")

    trace = Trace(name=name, trace_id=trace_id, queue_manager=tracing_queue_manager(), metadata=metadata)
    log.debug(f"Created new trace: {trace.trace_id}")

    return trace


def create_span(
    name: str,
    span_id: Optional[str] = None,
    input: Optional[Dict[str, Any]] = None,
    output: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Optional[str]]] = None,
    trace: Optional[Union[BaseTrace, str]] = None,
    parent_span: Optional[BaseSpan] = None,
) -> BaseSpan:
    """Creates a new span instance.

    A span represents a single unit of work or operation within a trace. Spans
    can be nested to form a hierarchy.

    If tracing is disabled (via 'DISABLE_SCALE_TRACING' environment variable),
    a `NoOpSpan` is returned. Additionally, if no explicit `parent` (Trace or Span)
    is provided and there is no `current_trace()` active in the scope, a `NoOpSpan`
    will also be returned to prevent orphaned spans.

    When a span is started (e.g., via context manager or `start()`), it becomes
    the `current_span()` in the active scope.

    Args:
        name (str): A descriptive name for the span (e.g., "database_query",
                    "http_request").
        span_id (Optional[str]): An optional, user-defined ID for the span.
        input (Optional[dict[str, Any]], optional): A dictionary containing
            input data or parameters relevant to this span's operation. Defaults to None.
        output (Optional[dict[str, Any]], optional): A dictionary containing
            output data or results from this span's operation. Defaults to None.
        metadata (Optional[dict[str, Union[str, int, float, bool, None]]], optional):
            A dictionary for arbitrary key-value pairs providing additional
            context or annotations for the span. Values should be simple types.
            Defaults to None.
        trace (Optional[Union[BaseTrace, str]], optional): A `Trace` instance
            or a trace ID. Used for explicit control. Default to trace fetched
            from the active scope.
        parent_span (Optional[BaseSpan], optional): A `Span` instance. Like
            trace, used for explicit control. Defaults to span fetched from the
            active scope.

    Returns:
        BaseSpan: A `Span` instance if tracing is enabled and a valid trace context
                  exists, or a `NoOpSpan` otherwise.
    """
    queue_manager = tracing_queue_manager()
    parent_span_id: Optional[str] = None

    if parent_span is not None:
        trace_id = parent_span.trace_id
        parent_span_id = parent_span.span_id
    elif trace is not None:
        trace_id = trace if isinstance(trace, str) else trace.trace_id

        parent_span = Scope.get_current_span()
        parent_span_id = parent_span.span_id if parent_span else None
    else:
        trace = Scope.get_current_trace()
        parent_span = Scope.get_current_span()

        parent_span_id = parent_span.span_id if parent_span else None

        if trace is None:
            # need to think about default behavior here... do we create a trace, some other options?
            # I am leaning towards setting it as an option as sometimes people might want to be succinct or when we
            # build decorators we might want this functionality
            log.debug(f"attempting to create a span with no trace")
            return NoOpSpan(name=name, span_id=span_id, parent_span_id=parent_span_id)

        trace_id = trace.trace_id

    if is_disabled():
        return NoOpSpan(name=name, span_id=span_id, parent_span_id=parent_span_id, trace_id=trace_id)

    span = Span(
        name=name,
        span_id=span_id,
        parent_span_id=parent_span_id,
        trace_id=trace_id,
        input=input or {},
        output=output or {},
        metadata=metadata or {},
        queue_manager=queue_manager,
    )
    log.debug(f"Created new span: {span.span_id}")

    return span
