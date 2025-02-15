class Master:
    def __init__(self, deviation: int) -> None:
        self.deviation: int = deviation

class Servo(Master):
    def __init__(self, dev: int) -> None:
        super().__init__(deviation=dev)

servo = Servo(dev=0)
