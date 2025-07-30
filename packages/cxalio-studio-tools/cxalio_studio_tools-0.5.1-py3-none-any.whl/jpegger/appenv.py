from cx_tools.app import IAppEnvironment
from collections.abc import Sequence
from .simple_appcontext import SimpleAppContext


class AppEnv(IAppEnvironment):
    def __init__(self):
        super().__init__()
        self.app_name = "Jpegger"
        self.app_version = "0.5.1"
        self.context: SimpleAppContext

    def is_debug_mode_on(self):
        return self.context.debug_mode


appenv = AppEnv()
