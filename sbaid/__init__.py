"""
The main SBAid package. It is the entry point into the application
and contains only the application and all other packages.
"""

# There is some black magic happening here but when we import these
# just in time in the result generators the python interpreter
# (like the actual INTERPRETER that should handle everything gracefully
# not our program or anything) segfaults
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure

import sys
import asyncio
from typing import Coroutine, Any

from gi.repository import GLib
from gi.events import GLibEventLoopPolicy  # type: ignore

from sbaid.application import Application


class _Task(asyncio.Task[Any]):
    def __init__(self, coro: Coroutine[Any, Any, Any], **kwargs: Any) -> None:
        super().__init__(coro, **kwargs)

        self.add_done_callback(self.__done_callback)
        self.__idle_id = GLib.idle_add(lambda: GLib.SOURCE_CONTINUE)

    def __done_callback(self, task: '_Task') -> None:
        GLib.source_remove(self.__idle_id)


def __task_factory(event_loop: asyncio.AbstractEventLoop,
                   coro: Coroutine[Any, Any, Any], **kwargs: Any) -> asyncio.Task[Any]:
    return _Task(coro, **kwargs)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    asyncio.get_event_loop().set_task_factory(__task_factory)
    app = Application()
    app.run(sys.argv)
    asyncio.set_event_loop_policy(None)
