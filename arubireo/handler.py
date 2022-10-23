from arubireo import execute


class MessageHandler:
    def parse(self, message: str, user_id: str) -> str:
        res = ""
        if not self._is_command(message):
            return ""

        name, msg = message.split(" ", 1)
        name = name[1:]
        if name in execute:
            res = execute[name](msg=msg, user_id=user_id)
        return res

    def _is_command(self, message: str) -> bool:
        return len(message) > 2 and message[0] == "!" and " " in message
