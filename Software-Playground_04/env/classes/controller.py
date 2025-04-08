import socket
from typing import Optional, Literal

# Config
from env.config import config

# Func
from env.func.DEBUG import dprint

class Controller:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", config.port))
        self.sock.listen(1)  # Listen for one client connection
        dprint(f"Controller listening on port {config.port:_}...")

        self.controller_sock, _ = self.sock.accept()
        dprint(f"Controller connected! Waiting for inputs...")

    def get_input(self) -> Optional[Literal["step-backwards", "step-forwards", "turn-left", "turn-right", "sidestep-left", "sidestep-right", "lower", "lift","normal"]]:
        return config.controller_map.get(self.controller_sock.recv(config.bufsize), None) or self.get_input()
