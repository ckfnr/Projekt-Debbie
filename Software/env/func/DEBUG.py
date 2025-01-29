# Config
from env.config import config

def dprint(msg: str) -> None:
    if config.debug:
        print(msg)
