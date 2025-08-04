"""
The main SBAid package. It is the entry point into the application
and contains only the application and the other packages.
"""

import sys
import asyncio

from gi.events import GLibEventLoopPolicy  # type: ignore

from sbaid.application import Application

if __name__ == '__main__':
    asyncio.set_event_loop_policy(GLibEventLoopPolicy())
    app = Application()
    app.run(sys.argv)
