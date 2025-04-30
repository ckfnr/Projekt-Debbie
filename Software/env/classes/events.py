from threading import Event

class StopEvent:
    def __init__(self) -> None:
        self._event: Event = Event()

    def set(self)    -> None:
        self._event.set()

    def reset(self)  -> None:
        self._event.clear()

    def is_set(self) -> bool:
        return self._event.is_set()
