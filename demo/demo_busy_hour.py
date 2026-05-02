"""
Simulation demo for busy hour logic.
"""
import sys
import os
import random
import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elevator_system import ElevatorSystem


def simulate_busy_hour_demo() -> None:
    """
    Simulate elevator requests during a transition from normal to busy hours.
    """
    system = ElevatorSystem()

    # We will simulate a window of time
    # Let's say we simulate from 7:30 AM to 10:00 AM in 5-minute increments
    start_time = datetime.datetime(2026, 5, 3, 7, 30)

    print(f"{'Time':<10} | {'Status':<10} | {'Requests'}")
    print("-" * 40)

    for i in range(30):  # 30 steps of 5 minutes = 150 minutes (2.5 hours)
        current_time = start_time + datetime.timedelta(minutes=i * 5)
        current_time_only = current_time.time()

        is_busy = system.is_busy_hour(current_time_only)
        status = "BUSY" if is_busy else "Normal"

        # In busy hours, we have more requests
        num_requests = random.randint(1, 3) if is_busy else random.randint(0, 1)

        request_floors = []
        for _ in range(num_requests):
            floor = random.randint(1, 10)
            system.request_elevator(floor)
            request_floors.append(floor)

        print(f"{current_time_only.strftime('%H:%M'):<10} | {status:<10} | "
              f"{num_requests} requests for floors {request_floors}")

        # Step the system
        system.step()


if __name__ == "__main__":
    simulate_busy_hour_demo()
