"""
Demo for fire drill logic including blocking and fireman override.
"""
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elevator_system import ElevatorSystem


def demo_fire_drill() -> None:
    """
    Demonstrate how the system behaves during a fire drill.
    """
    system = ElevatorSystem()

    print("--- Normal Operation ---")
    system.request_elevator(5)
    system.step()
    system.status()

    print("\n--- ACTIVATE FIRE DRILL ---")
    system.activate_fire_drill()
    system.status()

    print("\n--- Try normal request during fire drill ---")
    system.request_elevator(7)

    print("\n--- Fireman Override ---")
    system.fireman_override('C', 10)

    print("\n--- Running Simulation (10 steps) ---")
    for i in range(1, 11):
        print(f"\nStep {i}:")
        system.step()
        # system.status()

    print("\n--- Status after 10 steps ---")
    system.status()

    print("\n--- DEACTIVATE FIRE DRILL ---")
    system.deactivate_fire_drill()
    system.status()

    print("\n--- Normal request again ---")
    system.request_elevator(2)


if __name__ == "__main__":
    demo_fire_drill()
