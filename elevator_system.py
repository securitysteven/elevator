import datetime
from typing import Dict, List, Optional, Tuple
from elevator import Elevator


class ElevatorSystem:
    """
    Manages a collection of elevators and handles dispatching requests.
    """

    def __init__(self):
        """
        Initialize the ElevatorSystem with 6 elevators and predefined busy hours.
        """
        self.elevators: Dict[str, Elevator] = {
            'A': Elevator('A', 'North'),
            'B': Elevator('B', 'North'),
            'C': Elevator('C', 'North', is_emergency=True),
            'D': Elevator('D', 'South'),
            'E': Elevator('E', 'South'),
            'F': Elevator('F', 'South', is_emergency=True),
        }
        self.busy_hours: List[Tuple[datetime.time, datetime.time]] = [
            (datetime.time(8, 0), datetime.time(9, 30)),
            (datetime.time(11, 45), datetime.time(13, 30)),
            (datetime.time(4, 30), datetime.time(5, 30)),
        ]
        self.fire_drill_active: bool = False

    def activate_fire_drill(self) -> None:
        """
        Activate a fire drill: block all elevators and send them to the ground floor.
        """
        print("\n--- FIRE DRILL ACTIVATED ---")
        self.fire_drill_active = True
        for elevator in self.elevators.values():
            # Clear existing requests first
            elevator.requests.clear()
            elevator.is_blocked = True
            # Send all to the ground floor (floor 0)
            elevator.add_request(0, bypass_block=True)

    def deactivate_fire_drill(self) -> None:
        """
        Deactivate the fire drill and restore normal operation.
        """
        print("\n--- FIRE DRILL DEACTIVATED ---")
        self.fire_drill_active = False
        for elevator in self.elevators.values():
            elevator.is_blocked = False
            elevator.is_fireman_mode = False

    def fireman_override(self, elevator_name: str, floor: int) -> None:
        """
        Allow a fireman to override an elevator's block during a fire drill.

        Args:
            elevator_name (str): The name of the elevator to override.
            floor (int): The target floor for the fireman.
        """
        if not self.fire_drill_active:
            print("Fire drill is not active. No need for fireman override.")
            return

        if elevator_name in self.elevators:
            elevator = self.elevators[elevator_name]
            elevator.is_fireman_mode = True
            elevator.add_request(floor)
            print(f"Fireman override: Elevator {elevator_name} dispatched to floor {floor}")
        else:
            print(f"Elevator {elevator_name} not found.")

    def is_busy_hour(self, current_time: Optional[datetime.time] = None) -> bool:
        """
        Check if the specified time (or current time) falls within busy hours.

        Args:
            current_time (Optional[datetime.time]): The time to check. Defaults to now.

        Returns:
            bool: True if it's a busy hour, False otherwise.
        """
        if current_time is None:
            current_time = datetime.datetime.now().time()

        for start, end in self.busy_hours:
            if start <= current_time <= end:
                return True
        return False

    def request_elevator(self, floor: int, side: Optional[str] = None, is_priority: bool = False) -> None:
        """
        Request an elevator to a specific floor.

        Args:
            floor (int): The floor being requested.
            side (Optional[str]): If specified, only elevators on this side will respond.
            is_priority (bool): If True, only emergency elevators (C and F) will respond.
        """
        def filter_elevators(emergency_only: bool) -> List[Elevator]:
            return [e for e in self.elevators.values() if e.is_emergency == emergency_only and
                    (not side or e.side.lower() == side.lower())]

        # Primary selection: emergency elevators for priority, non-emergency for normal
        eligible = filter_elevators(is_priority)

        # Fallback: if normal request has no non-emergency elevators, use emergency ones
        if not eligible and not is_priority:
            eligible = filter_elevators(True)

        # Filter available (not blocked) elevators
        available = [e for e in eligible if not e.is_blocked or e.is_fireman_mode]

        if not available:
            msg = "Cannot request elevator during fire drill." if self.fire_drill_active else "No elevators available."
            print(msg)
            return

        best_elevator = min(available, key=lambda e: abs(e.current_floor - floor))
        if best_elevator.add_request(floor):
            prefix = "PRIORITY " if is_priority else ""
            print(f"{prefix}Request for floor {floor} assigned to Elevator {best_elevator.name} ({best_elevator.side})")

    def step(self) -> None:
        """Move all elevators one step."""
        for elevator in self.elevators.values():
            elevator.move()

    def status(self) -> None:
        """Print the current status of all elevators."""
        for elevator in self.elevators.values():
            print(elevator)
