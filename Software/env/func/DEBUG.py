from typing import Any

# Config
from env.config import config

def dprint(msg: Any) -> None:
    if config.debug:
        print(msg)

    #ToDo: Add logging
