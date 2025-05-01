import socket
import threading
import time
from typing import Optional, Literal

# Config
from env.config import config

# Func
from env.func.DEBUG import dprint

class Controller:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((config.ip, config.port))
        self.sock.listen(1)
        dprint(f"Controller listening on {config.ip}:{config.port:_}...")

        self.controller_sock: Optional[socket.socket] = None
        self._last_input: Optional[Literal["step-backwards", "step-forwards", "turn-left", "turn-right", "sidestep-left", "sidestep-right", "lower", "lift", "normal", "RESET"]] = None
        self._last_heartbeat: Optional[float] = None

        self._accept_connection()
        self._start_receiver_thread()
        dprint(f"Controller initialized!")

    def _accept_connection(self) -> None:
        while True:
            try:
                self.controller_sock, addr = self.sock.accept()
                dprint(f"Controller connected from {addr}! Waiting for inputs...")
                break
            except socket.error as e:
                dprint(f"Connection accept failed: {e}")
                time.sleep(1)

    def _start_receiver_thread(self) -> None:
        def update() -> None:
            while True:
                try:
                    assert self.controller_sock is not None, "Controller socket is None"

                    # Set a timeout for the socket to avoid blocking indefinitely
                    raw: bytes = self.controller_sock.recv(config.bufsize)
                    if not raw:
                        raise ConnectionResetError("Client disconnected")

                    data: Optional[Literal[
                        "step-backwards", "step-forwards", "turn-left", "turn-right",
                        "sidestep-left", "sidestep-right", "lower", "lift",
                        "normal", "RESET", "HEARTBEAT"
                    ]] = config.controller_map.get(raw, None)

                    if data == "HEARTBEAT":
                        self._last_heartbeat = time.time()
                        dprint(f"{config.color_green}Heartbeat received!{config.color_reset}")
                    elif data is not None:
                        self._last_input = data

                except (ConnectionResetError, socket.error) as e:
                    dprint(f"Connection lost: {e}. Waiting for reconnection...")
                    self._accept_connection()

        threading.Thread(target=update, daemon=True).start()

    @property
    def last_input(self) -> Optional[Literal[
        "step-backwards", "step-forwards", "turn-left", "turn-right",
        "sidestep-left", "sidestep-right", "lower", "lift",
        "normal", "RESET"
    ]]:
        return self._last_input

    def __del__(self) -> None:
        if hasattr(self, "controller_sock") and self.controller_sock:
            self.controller_sock.close()
        if hasattr(self, "sock") and self.sock:
            self.sock.close()
