class Config:
    def __init__(self) -> None:
        # Thigh
        # Max values
        self.max_thigh_angle_rf: int = 120  # Thigh right front
        self.max_thigh_angle_rb: int = 120  # Thigh right back
        self.max_thigh_angle_lf: int = 120  # Thigh left front
        self.max_thigh_angle_lb: int = 120  # Thigh left back
        # Min values
        self.min_thigh_angle_rf: int = 40   # Thigh right front
        self.min_thigh_angle_rb: int = 40   # Thigh right back
        self.min_thigh_angle_lf: int = 40   # Thigh left front
        self.min_thigh_angle_lb: int = 40   # Thigh left back


        # Lower leg
        # Max values
        self.max_lower_leg_angle_rf: int = 130  # Lower leg right front
        self.max_lower_leg_angle_rb: int = 130  # Lower leg right back
        self.max_lower_leg_angle_lf: int = 130  # Lower leg left front
        self.max_lower_leg_angle_lb: int = 130  # Lower leg left back
        # Min values
        self.min_lower_leg_angle_rf: int = 60   # Lower leg right front
        self.min_lower_leg_angle_rb: int = 60   # Lower leg right back
        self.min_lower_leg_angle_lf: int = 60   # Lower leg left front
        self.min_lower_leg_angle_lb: int = 60   # Lower leg left back


        # Side axis left
        # Max values
        self.max_side_axis_angle_rf: int = 45  # Side axis right front
        self.max_side_axis_angle_rb: int = 45  # Side axis right back
        self.max_side_axis_angle_lf: int = 45  # Side axis left front
        self.max_side_axis_angle_lb: int = 45  # Side axis left back
        # Min values
        self.min_side_axis_angle_rf: int = 15  # Side axis right front
        self.min_side_axis_angle_rb: int = 15  # Side axis right back
        self.min_side_axis_angle_lf: int = 15  # Side axis left front
        self.min_side_axis_angle_lb: int = 15  # Side axis left back


        # Servo general (default)
        self.servo_channel_count: int = 16    # Channels of the servo controller
        self.servo_normal_position: int = 90  # Normal position of all servos
        self.servo_default_steps: int = 5     # Number of steps during movement (MUSTN'T BE 0!!!)


        # Set up channels
        # Right front
        self.servo_channel_RFT: int = 0   # Thigh
        self.servo_channel_RFL: int = 1   # Lower leg
        self.servo_channel_RFS: int = 2   # Side axis
        # Right back
        self.servo_channel_RBT: int = 4   # Thigh
        self.servo_channel_RBL: int = 5   # Lower leg
        self.servo_channel_RBS: int = 6   # Side axis
        # Left front
        self.servo_channel_LFT: int = 8   # Thigh
        self.servo_channel_LFL: int = 9  # Lower leg
        self.servo_channel_LFS: int = 10  # Side axis
        # Left back
        self.servo_channel_LBT: int = 12  # Thigh
        self.servo_channel_LBL: int = 13  # Lower leg
        self.servo_channel_LBS: int = 14  # Side axis


        # Servo deviations
        # Thighs
        self.servo_deviation_thigh_rf: int = 0      # Deviation for thigh right front     (default = 0)
        self.servo_deviation_thigh_rb: int = 0      # Deviation for thigh right back      (default = 0)
        self.servo_deviation_thigh_lf: int = 0      # Deviation for thigh left front      (default = 0)
        self.servo_deviation_thigh_lb: int = 0      # Deviation for thigh right back      (default = 0)
        # Lower legs
        self.servo_deviation_lower_leg_rf: int = 0  # Deviation for lower leg right front (default = 0)
        self.servo_deviation_lower_leg_rb: int = 0  # Deviation for lower leg right back  (default = 0)
        self.servo_deviation_lower_leg_lf: int = 0  # Deviation for lower leg left front  (default = 0)
        self.servo_deviation_lower_leg_lb: int = 0  # Deviation for lower leg left back   (default = 0)
        # Side axis
        self.servo_deviation_side_axis_rf: int = 0  # Deviation for side axis right front (default = 0)
        self.servo_deviation_side_axis_rb: int = 0  # Deviation for side axis right back  (default = 0)
        self.servo_deviation_side_axis_lf: int = 0  # Deviation for side axis left front  (default = 0)
        self.servo_deviation_side_axis_lb: int = 0  # Deviation for side axis left back   (default = 0)


config = Config()

#ToDo: Measure and update values
