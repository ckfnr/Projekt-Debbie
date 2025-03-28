
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
        self.servo_normal_position: int = 90             # Normal position of all servos
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
                "min_lower_leg": 80,
                "max_lower_leg": 120,
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
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 80,
                "max_lower_leg": 120,
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
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 80,
                "max_lower_leg": 120,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 12,
                "lower_leg": -59,
                "side_axis": -22,
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
                "min_thigh": 40,
                "max_thigh": 120,
                "min_lower_leg": 80,
                "max_lower_leg": 120,
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
