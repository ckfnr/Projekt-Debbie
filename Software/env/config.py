
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
from env.types.typing import LegConfigDict

class Config:
    def __init__(self) -> None:
        # Colors
        self.color_reset: str =  "\033[0m"
        self.color_green: str =  "\033[32m"
        self.color_yellow: str = "\033[33m"
        self.color_red: str =    "\033[31m"

        # Database settings
        self.db_file: str = "movement.sqlite3"

        # Developer settings
        self.debug: bool = True

        # Servo general (default)
        self.servo_channel_count: int = 16               # Channel amount of the servo controller
        self.servo_normal_position: int = 0              # Normal position of all servos
        self.servo_default_normalize_speed: float = 3.0  # How many seconds the servos should need to normalize their position
        self.servo_default_speed: float = 1.0            # Default speed of the servos
        # self.servo_stopping_threshold: float = 5.0     # The threshold that determines when the servo movement should stop.  (The smaller the more accurate); Shouldn't be too small to ensure functionality!
        self.max_legs: int = 4                           # How many legs DEBBIE has

        # Coordinate calculation settings
        self.number_a: float = -0.5                      # Multiplier for the radius of the circle movement
        self.coord_multiplier: float = 4/3               # Multiplier for the coordinate system of the servos

        # Gyroscope general (default)
        self.deviation_x: float = -103.3
        self.deviation_y: float = 1.6
        self.deviation_z: float = -2.1

        # Decorator config
        self.max_lru_cache: int = 100                     # The maximum amount of cache entries for the lru decorator

        # MMT-File settings
        self.duration_pattern: Pattern = compile(r"seconds=(\d+(\.\d+)?)")
        self.coordinate_pattern: Pattern = compile(r"(\w+): ([\w=,\.\-\s]+)")
        self.wait_pattern: Pattern = compile(r"WAIT=\s*(-?\d*\.\d+|\d+\.?)\s*")
        self.mmt_default_path: str = "movements"
        self.auto_parse_startup: bool = True

        # Controller settings
        self.bufsize: int = 1024                  # Buffer size for the controller
        self.port   : int = 58_000                # Port for the controller
        self.ip     : str = "0.0.0.0"             # IP for the controller
        self.max_heartbeat_interval: float = 2.0  # The maximum time in seconds between two heartbeats
        self.controller_map: dict[bytes, Literal["step-backwards", "step-forwards", "turn-left", "turn-right", "sidestep-left", "sidestep-right", "lower", "lift", "normal", "RESET", "HEARTBEAT"]] = {
            b"\x00": "HEARTBEAT",       # Heartbeat
            b"\x01": "step-forwards",   # Walk forwards
            b"\x02": "step-backwards",  # Walk backwards
            b"\x03": "turn-left",       # Turn left
            b"\x04": "turn-right",      # Turn right
            b"\x05": "sidestep-left",   # Sidestep left
            b"\x06": "sidestep-right",  # Sidestep right
            b"\x07": "lower",           # Lower the legs
            b"\x08": "lift",            # Lift the legs
            b"\x09": "normal",          # Normal position
            b"\xff": "RESET",           # Stop all movements
        }

        # Leg length settings
        self.z_def : float = -170  # The default z position of the leg in mm
        self.d_s   : float =   20
        self.d_ys  : float =   25
        self.d_cpm : float =   13
        self.f_w   : float =   16
        self.l_1   : float =  114
        self.l_2   : float =  100
        self.l_3   : float =   27
        self.l_4   : float =   97
        self.l_5   : float =   31
        self.l_6   : float =   46
        self.l_7   : float =   25
        self.l_8   : float =   38
        self.l_9   : float =   24

        # Step settings
        self.max_points : int   =   10  # The maximum amount of points for the circle movement
        self.step_width : float = 50.0  # The width of the step in mm
        self.step_height: float = 40.0  # The height of the step in mm
        self.smoothness : float = -0.5  # The smoothness of the circle movement
        self.duration   : float =  0.1  # The duration of the movement in seconds
        self.coord_deviation: tuple[float, float, float] = (0.0, 0.0, 0.0)  # xyz in mm

        # Step map settings
        # (left_front, left_back, right_front, right_back)
        self.step_map_angles: dict[Literal["step-forward", "step-backward", "sidestep-left", "sidestep-right", "turn-left", "turn-right"], dict[Literal["left-front", "left-back", "right-front", "right-back"], int]] = {
            # Steps
            "step-forward"  : {"left-front": 0  , "left-back": 0   , "right-front": 0  , "right-back": 0  },
            "sidestep-right": {"left-front": 90 , "left-back": 90  , "right-front": 270, "right-back": 270},
            "step-backward" : {"left-front": 180, "left-back": 180 , "right-front": 0  , "right-back": 0  },
            "sidestep-left" : {"left-front": 270, "left-back": 270 , "right-front": 90 , "right-back": 90 },

            # Turn left/right
            "turn-left"     : {"left-front": 270, "left-back": 90  , "right-front": 270, "right-back": 90 },
            "turn-right"    : {"left-front": 90 , "left-back": 270 , "right-front": 90 , "right-back": 270},
        }

        # Leg settings
        # All values have to be integer!!!
        self.leg_configuration_rf: LegConfigDict = {
            "channels": {
                "thigh": 0,
                "lower_leg": 1,
                "side_axis": 2,
            },
            "angles": {
                "min_thigh": 60,
                "max_thigh": 125,
                "min_lower_leg": 55,
                "max_lower_leg": 130,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": -12,
                "lower_leg": 0,
                "side_axis": 2,
            },
            "mirrored":{
                "thigh": False,
                "lower_leg": False,
                "side_axis": False,
            }
        }
        self.leg_configuration_rb: LegConfigDict = {
            "channels": {
                "thigh": 8,
                "lower_leg": 9,
                "side_axis": 10,
            },
            "angles": {
                "min_thigh": 60,
                "max_thigh": 125,
                "min_lower_leg": 55,
                "max_lower_leg": 130,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 0,
                "lower_leg": -3,
                "side_axis": -20,  # -20
            },
            "mirrored":{
                "thigh": False,
                "lower_leg": False,
                "side_axis": True,
            }
        }
        self.leg_configuration_lf: LegConfigDict = {
            "channels": {
                "thigh": 4,
                "lower_leg": 5,
                "side_axis": 6,
            },
            "angles": {
                "min_thigh": 60,
                "max_thigh": 125,
                "min_lower_leg": 55,
                "max_lower_leg": 130,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": 0,        # 12
                "lower_leg": 0,    # 59  #? Was this negative?
                "side_axis": -22,  # -22
            },
            "mirrored":{
                "thigh": True,
                "lower_leg": True,
                "side_axis": True,
            }
        }
        self.leg_configuration_lb: LegConfigDict = {
            "channels": {
                "thigh": 12,
                "lower_leg": 13,
                "side_axis": 14,
            },
            "angles": {
                "min_thigh": 60,
                "max_thigh": 125,
                "min_lower_leg": 55,
                "max_lower_leg": 130,
                "min_side_axis": 70,
                "max_side_axis": 130,
            },
            "deviations": {
                "thigh": -3,
                "lower_leg": -15,
                "side_axis": 10,
            },
            "mirrored":{
                "thigh": True,
                "lower_leg": True,
                "side_axis": False,
            }
        }

config = Config()
