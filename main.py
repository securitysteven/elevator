"""
Main entry point for the elevator simulation system.
"""
from elevator_system import ElevatorSystem


def main() -> None:
    """
    Run a basic simulation of the elevator system.
    """
    system = ElevatorSystem()

    print("--- Initial Status ---")
    system.status()

    is_busy = system.is_busy_hour()
    print(f"\nCurrently Busy Hour: {'Yes' if is_busy else 'No'}")

    print("\n--- Requesting Elevators ---")
    # Request from North side to floor 5
    system.request_elevator(5, side='North')
    # Request from South side to floor 3
    system.request_elevator(3, side='South')
    # Request from any side to floor 10
    system.request_elevator(10)
    # Priority request for VIP (floor 7)
    system.request_elevator(7, is_priority=True)

    print("\n--- Running Simulation (10 steps) ---")
    for i in range(1, 11):
        print(f"\nStep {i}:")
        system.step()
        # system.status() # Uncomment to see status at each step

    print("\n--- Final Status ---")
    system.status()


if __name__ == "__main__":
    main()
