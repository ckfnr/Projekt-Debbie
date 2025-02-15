from env.func.movement import Movement

m = Movement()
d: int = 1

m.normalize_all_legs()

while True:
    # Set target angles for each servo
    for leg in m.all_legs:
        leg.thigh.set(target_angle=120, duration=d)
        leg.lower_leg.set(target_angle=80, duration=d)
        leg.side_axis.set(target_angle=130, duration=d)
    
    # Start all movements
    for leg in m.all_legs:
        leg.thigh.start()
        leg.lower_leg.start()
        leg.side_axis.start()
    
    # Wait for all legs to finish their movements
    for leg in m.all_legs:
        leg.thigh.join()
        leg.lower_leg.join()
        leg.side_axis.join()

    # Normalize all legs again
    m.normalize_all_legs(duration_s=d)
