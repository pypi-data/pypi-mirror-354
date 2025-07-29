"""Delta Cycle

Credit to David Beazley's "Build Your Own Async" tutorial for inspiration:
https://www.youtube.com/watch?v=Y4Gt3Xjd7G8
"""

import logging
from logging import Filter, LogRecord

from ._event import Event
from ._loop import (
    Loop,
    LoopState,
    changed,
    create_task,
    finish,
    get_current_task,
    get_loop,
    get_running_loop,
    irun,
    now,
    run,
    set_loop,
    sleep,
    touched,
)
from ._queue import Queue
from ._semaphore import BoundedSemaphore, Lock, Semaphore
from ._task import CancelledError, InvalidStateError, Task, TaskState
from ._task_group import TaskGroup
from ._variable import Aggregate, AggrItem, AggrValue, Singular, Value, Variable

# Customize logging
logger = logging.getLogger(__name__)


class DeltaCycleFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        try:
            loop = get_running_loop()
        except RuntimeError:
            record.time = -1
            record.taskName = None
        else:
            record.time = loop.time()
            record.taskName = loop.task().name
        return True


logger.addFilter(DeltaCycleFilter())


__all__ = [
    # loop
    "Loop",
    "LoopState",
    "changed",
    "create_task",
    "finish",
    "get_current_task",
    "get_loop",
    "get_running_loop",
    "irun",
    "now",
    "run",
    "set_loop",
    "sleep",
    "touched",
    # event
    "Event",
    # queue
    "Queue",
    # semaphore
    "BoundedSemaphore",
    "Lock",
    "Semaphore",
    # task
    "CancelledError",
    "InvalidStateError",
    "Task",
    "TaskState",
    # task_group
    "TaskGroup",
    # variable
    "Variable",
    "Value",
    "Singular",
    "Aggregate",
    "AggrItem",
    "AggrValue",
]
