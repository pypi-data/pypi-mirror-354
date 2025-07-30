import asyncio
from abc import ABC, abstractmethod

from rich.console import Console

from cx_studio.utils.tools import DoubleTrigger


class IAppEnvironment(ABC):

    def __init__(self):
        self.app_name = ""
        self.app_version = ""
        self.console = Console(stderr=True)

        self.wanna_quit_event = asyncio.Event()
        self.really_wanna_quit_event = asyncio.Event()

        self.interrupt_handler = DoubleTrigger()

        @self.interrupt_handler.on("first_triggered")
        def __when_wanna_quit():
            self.whisper("[red]触发中断信号…[/]")
            # self.wanna_quit = True
            self.wanna_quit_event.set()

        @self.interrupt_handler.on("second_triggered")
        def __when_really_wanna_quit():
            self.whisper("[red]检测到强制中断信号…[/]")
            # self.really_wanna_quit = True
            self.really_wanna_quit_event.set()

    def handle_interrupt(self, _sig, _frame):
        self.interrupt_handler.trigger()

    # @abstractmethod
    def is_debug_mode_on(self):
        return False

    # @abstractmethod
    def start(self):
        self.whisper(
            "{} v{} environment started.".format(self.app_name, self.app_version)
        )

    # @abstractmethod
    def stop(self):
        self.whisper(
            "{} v{} environment stopped.".format(self.app_name, self.app_version)
        )

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.whisper("Bye ~")
        return False

    def say(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def whisper(self, *args, **kwargs):
        if self.is_debug_mode_on():
            kwargs["style"] = "dim"
            kwargs["highlight"] = False
            self.console.print(*args, **kwargs)
