
       #####################################
    ###                                     ###
  ##                                           ##
 ##                                             ##
##        _   _           _            _         ##
##       | \ | |         | |          | |        ##
##       |  \| |   ___   | |_    ___  | |        ##
##       | . ` |  / _ \  | __|  / _ \ | |        ##
##       | |\  | | (_) | | |_  |  __/ |_|        ##
##       |_| \_|  \___/   \__|  \___| (_)        ##
##                                               ##
##                                               ##
##      Do not change any values in this         ##
##      section, unless you know exactly         ##
##      what you are doing.                      ##
##                                               ##
##      Every change you make could              ##
##      destroy the whole project!               ##
 ##                                             ##
  ##                                           ##
    ###                                     ###
       #####################################



from re import compile, Pattern
from typing import Literal

class Config:
    def __init__(self) -> None:
        # Colors
        self.color_reset: str =  "\033[0m"
        self.color_green: str =  "\033[32m"
        self.color_yellow: str = "\033[33m"

        # Database settings
        self.db_file: str = "movement.sqlite3"

        # Developer settings
        self.debug: bool = True

        # Servo general (default)
        self.servo_channel_count: int = 16               # Channel amount of the servo controller
        self.servo_normal_position: int = 0              # Normal position of all servos
        self.servo_default_normalize_speed: float = 3.0  # How many seconds the servos should need to normalize their position
        self.servo_default_speed: float = 1.0            # Default speed of the servos
        self.servo_stopping_treshhold: float = 0.5       # The threshold that determines when the servo movement should stop.  (The smaller the more accurate)
        self.max_legs: int = 4                           # How many legs DEBBIE has

        # Coordinate calculation settings
        self.number_a: float = -0.5                      # Multiplier for the radius of the circle movement

        # Gyroscope general (default)
        self.deviation_x: float = -103.3
        self.deviation_y: float = 1.6
        self.deviation_z: float = -2.1

        # Decorator config
        self.max_lru_cache: int = 50                     # The maximum amount of cache entries for the lru decorator

        # MMT-File settings
        self.duration_pattern: Pattern = compile(r"seconds=(\d+(\.\d+)?)")
        self.coordinate_pattern: Pattern = compile(r"(\w+): ([\w=,\.\-\s]+)")
        self.wait_pattern: Pattern = compile(r"WAIT=\s*(-?\d*\.\d+|\d+\.?)\s*")
        self.mmt_default_path: str = "movements"
        self.auto_parse_startup: bool = True

        # Controller settings
        self.bufsize: int = 1024
        self.port: int = 58_000
        self.controller_map: dict[bytes, Literal["step-backwards", "step-forwards", "turn-left", "turn-right", "sidestep-left", "sidestep-right", "lower", "lift","normal"]] = {
            b"\x01": "step-forwards",   # Walk forwards
            b"\x02": "step-backwards",  # Walk backwards
            b"\x03": "turn-left",       # Turn left
            b"\x04": "turn-right",      # Turn right
            b"\x05": "sidestep-left",   # Sidestep left
            b"\x06": "sidestep-right",  # Sidestep right
            b"\x07": "lower",           # Lower the legs
            b"\x08": "lift",            # Lift the legs
            b"\x09": "normal",          # Normal position
        }


        # Leg configurations
        self.l1: float = 114
        self.l2: float = 100
        self.l3: float = 27
        self.l4: float = 107
        self.l5: float = 27
        self.l6: float = 36
        self.l7: float = 24
        self.l8: float = 38
        self.l9: float = 24
        self.ds: float = 20
        self.epsilon: float = 45
        self.coord_deviation: tuple[float, float, float] = (-20.0, 0.0, -180.0)  # xyz in mm

        # All values have to be integer!!!
        self.leg_configuration_rf: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 0,
                "lower_leg": 1,
                "side_axis": 2,
            },
            "angles": {
                "min_thigh": 50,
                "max_thigh": 110,
                "min_lower_leg": 90,
                "max_lower_leg": 145,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 17,
                "lower_leg": 15,
                "side_axis": 0,
            },
            "mirrored":{
                "thigh": False,
                "lower_leg": False,
                "side_axis": False,
            }
        }
        self.leg_configuration_rb: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 8,
                "lower_leg": 9,
                "side_axis": 10,
            },
            "angles": {
                "min_thigh": 50,
                "max_thigh": 120,
                "min_lower_leg": 70,
                "max_lower_leg": 100,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 12,
                "lower_leg": 30,
                "side_axis": -20,
            },
            "mirrored":{
                "thigh": False,
                "lower_leg": False,
                "side_axis": True,
            }
        }
        self.leg_configuration_lf: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 4,
                "lower_leg": 5,
                "side_axis": 6,
            },
            "angles": {
                "min_thigh": 50,
                "max_thigh": 120,
                "min_lower_leg": 70,
                "max_lower_leg": 100,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 12,       # 12
                "lower_leg": -59,  # 59  #? Was this negative?
                "side_axis": -22,  # -22
            },
            "mirrored":{
                "thigh": True,
                "lower_leg": True,
                "side_axis": True,
            }
        }
        self.leg_configuration_lb: dict[str, dict[str, int]] = {
            "channels": {
                "thigh": 12,
                "lower_leg": 13,
                "side_axis": 14,
            },
            "angles": {
                "min_thigh": 50,
                "max_thigh": 120,
                "min_lower_leg": 70,
                "max_lower_leg": 100,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 15,
                "lower_leg": -45,
                "side_axis": 10,
            },
            "mirrored":{
                "thigh": True,
                "lower_leg": True,
                "side_axis": False,
            }
        }

config = Config()
