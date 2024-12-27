class Config:
    def __init__(self) -> None:
        # Servo general (default)
        self.servo_channel_count: int = 16              # Channels of the servo controller
        self.servo_normal_position: int = 90            # Normal position of all servos
        self.servo_default_steps: int = 10              # Number of steps during movement (MUSTN'T BE 0!!! --> Otherwise will raise DevisionError) A high amount will make the movement smoother
        self.servo_default_normalize_speed: float = 10  # How many seconds the servos should need to normalize their position
        self.auto_normalize_at_startup: bool = True     # If DEBBIE will normalize its servos at startup
        self.servo_stopping_treshhold: float = 0.1      # The threshold that determines when the servo movement should stop.  (The smaller the more accurate)

        # Leg configurations
        # All values have to be integer!!!
        self.leg_configuration_rf: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 0,
                "lower_leg": 1,
                "side_axis": 2,
            },
            "angles": {
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 60,
                "max_lower_leg": 130,
                "min_side_axis": 15,
                "max_side_axis": 45,
            },
            "deviations": {
                "thigh": 0,
                "lower_leg": 0,
                "side_axis": 0,
            }
        }
        self.leg_configuration_rb: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 8,
                "lower_leg": 9,
                "side_axis": 10,
            },
            "angles": {
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 60,
                "max_lower_leg": 130,
                "min_side_axis": 15,
                "max_side_axis": 45,
            },
            "deviations": {
                "thigh": 0,
                "lower_leg": 0,
                "side_axis": 0,
            }
        }
        self.leg_configuration_lf: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 4,
                "lower_leg": 5,
                "side_axis": 6,
            },
            "angles": {
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 60,
                "max_lower_leg": 130,
                "min_side_axis": 15,
                "max_side_axis": 45,
            },
            "deviations": {
                "thigh": 0,
                "lower_leg": 0,
                "side_axis": 0,
            }
        }
        self.leg_configuration_lb: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 12,
                "lower_leg": 13,
                "side_axis": 14,
            },
            "angles": {
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 60,
                "max_lower_leg": 130,
                "min_side_axis": 15,
                "max_side_axis": 45,
            },
            "deviations": {
                "thigh": 0,
                "lower_leg": 0,
                "side_axis": 0,
            }
        }

config = Config()

#ToDo: Measure and update values
