from env.func.movement import Movement

movement = Movement()

movement.walk_forward(distance_cm=100, duration_s=10)  # Walks 100 cm forward within 10 seconds
movement.walk_backward(distance_cm=50, duration_s=5)   # Walks 50 cm backward within 5 seconds
