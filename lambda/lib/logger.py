import datetime
import os
from enum import Enum
import json


class Logger():
    logs = []

    def __init__(self, name: str = None, **kwargs):
        pass

    class level(Enum):
        DEBUG = 1,
        INFO = 2,
        ERROR = 3

    def debug(self, message: str):
        time = datetime.datetime.now()
        self.logs.append(f"{time}:DEBUG:{message}")

    def info(self, message: str):
        time = datetime.datetime.now()
        self.logs.append(f"{time}:INFO:{message}")

    def error(self, message: str):
        time = datetime.datetime.now()
        self.logs.append(f"{time}:ERROR:{message}")

    def write(self, status: bool):
        log_level = self.level[os.getenv("LOG_LEVEL", "INFO")].value

        final = []
        for item in self.logs:
            if ":DEBUG:" in item:
                msg_level = self.level.DEBUG.value
            elif ":INFO:" in item:
                msg_level = self.level.INFO.value
            elif ":ERROR:" in item:
                msg_level = self.level.ERROR.value

            if msg_level >= log_level:
                final.append(item)

        final_log = {
            "status": str(status),
            "logs": final
        }
        print(json.dumps(final_log))
