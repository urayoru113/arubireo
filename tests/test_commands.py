import re

from arubireo import commands
from arubireo.commands import __commands__

execute = {command: getattr(commands, command) for command in __commands__}


def test_echo():
    assert "hello" == execute["echo"](msg="hello")


def test_roll():
    assert execute["roll"](msg="-6") == ""
    assert execute["roll"](msg="4").isdigit()
    assert execute["roll"](msg="   9   13  ").isdigit()
    assert execute["roll"](msg="   22   13  ") == ""
    assert execute["roll"](msg=" 0d5 ") == "[]"
    assert execute["roll"](msg=" 3d0 ") == ""
    assert re.search(r"^\-\d+$", execute["roll"](msg="   -19   -13  "))
    assert re.search(r"^\[\d+, \d+, \d+, \d+\]$", execute["roll"](msg=" 4D6 "))
