from arubireo.utils import Settings

env = Settings()

from arubireo import commands  # noqa: E402
from arubireo.commands import __commands__  # noqa: E402

execute = {command: getattr(commands, command) for command in __commands__}

__all__ = ["env"]
