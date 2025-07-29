import asyncio
import typing
from contextlib import contextmanager
from uuid import uuid4


TASK_ADDRESS_TO_TRACE_IDS: typing.Dict[int, typing.List[str]] = dict()


def _add_trace_id(task_address: int, trace_id_str: str):
    if task_address not in TASK_ADDRESS_TO_TRACE_IDS:
        TASK_ADDRESS_TO_TRACE_IDS[task_address] = [trace_id_str]
    else:
        TASK_ADDRESS_TO_TRACE_IDS[task_address].append(trace_id_str)


def _get_task_id() -> typing.Optional[int]:
    if asyncio.get_event_loop().is_running():
        task = asyncio.current_task()
        if task:
            return id(task)
    return None


def _remove_task_traces(task_address: int):
    if task_address in TASK_ADDRESS_TO_TRACE_IDS:
        del TASK_ADDRESS_TO_TRACE_IDS[task_address]


@contextmanager
def trace_id() -> typing.ContextManager[str]:
    task_address: int = _get_task_id()
    trace_id_str = str(uuid4())
    if task_address is not None:
        _add_trace_id(task_address, trace_id_str)
    try:
        if task_address is not None:
            yield trace_id_str
        else:
            yield
    finally:
        if task_address is not None:
            if trace_id_str in TASK_ADDRESS_TO_TRACE_IDS.get(task_address, []):
                TASK_ADDRESS_TO_TRACE_IDS[task_address].remove(trace_id_str)
                if not TASK_ADDRESS_TO_TRACE_IDS[task_address]:
                    del TASK_ADDRESS_TO_TRACE_IDS[task_address]


def get_trace_ids() -> typing.Optional[typing.List[str]]:
    task_address = _get_task_id()
    if task_address is None:
        return None
    return TASK_ADDRESS_TO_TRACE_IDS.get(task_address, [])


def add_trace_id(
    trace_id_str: typing.Optional[typing.Union[str, typing.List[str]]] = None
) -> typing.Optional[str]:
    task_address = _get_task_id()
    if task_address is None:
        return None
    if isinstance(trace_id_str, list):
        if task_address not in TASK_ADDRESS_TO_TRACE_IDS:
            TASK_ADDRESS_TO_TRACE_IDS[task_address] = trace_id_str[:]
        else:
            TASK_ADDRESS_TO_TRACE_IDS[task_address].extend(trace_id_str)
    else:
        if trace_id_str is None:
            trace_id_str = str(uuid4())
        _add_trace_id(task_address, trace_id_str)
    # Adding done callback for cleaning up trace IDs
    asyncio.current_task().add_done_callback(lambda _: _remove_task_traces(task_address))
    return trace_id_str
