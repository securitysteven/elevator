from enum import Enum
from typing import Set


class Direction(Enum):
    """Enum for elevator movement direction."""
    UP = 1
    DOWN = -1
    IDLE = 0


class Elevator:
    """
    Represents an independent elevator in the system.
    """

    def __init__(self, name: str, side: str, is_emergency: bool = False):
        """
        Initialize an Elevator instance.

        Args:
            name (str): The name of the elevator (e.g., 'A').
            side (str): The side of the hallway where the elevator is located.
            is_emergency (bool): Whether this is an emergency/priority elevator.
        """
        self.name: str = name
        self.side: str = side
        self.is_emergency: bool = is_emergency
        self.current_floor: int = 0
        self.direction: Direction = Direction.IDLE
        self.requests: Set[int] = set()
        self.is_blocked: bool = False
        self.is_fireman_mode: bool = False

    def add_request(self, floor: int, bypass_block: bool = False) -> bool:
        """
        Add a floor request to the elevator.

        Args:
            floor (int): The target floor.
            bypass_block (bool): If True, bypasses the fire drill block.

        Returns:
            bool: True if the request was added, False otherwise.
        """
        if self.is_blocked and not self.is_fireman_mode and not bypass_block:
            print(f"Elevator {self.name} is blocked due to fire drill. "
                  f"Request for floor {floor} ignored.")
            return False

        self.requests.add(floor)
        if self.direction == Direction.IDLE:
            if floor > self.current_floor:
                self.direction = Direction.UP
            elif floor < self.current_floor:
                self.direction = Direction.DOWN
        return True

    def move(self) -> None:
        """
        Move the elevator one floor in its current direction and update its state.
        """
        if self.is_blocked and not self.is_fireman_mode:
            # If blocked, it should stay put or go to floor 0 as handled by system.
            return

        if not self.requests:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.requests:
            print(f"Elevator {self.name} ({self.side}) arrived at floor {self.current_floor}")
            self.requests.remove(self.current_floor)
            
            if not self.requests:
                self.direction = Direction.IDLE
            else:
                # Decide next direction
                has_above = any(f > self.current_floor for f in self.requests)
                has_below = any(f < self.current_floor for f in self.requests)
                
                if self.direction == Direction.UP and not has_above:
                    self.direction = Direction.DOWN if has_below else Direction.IDLE
                elif self.direction == Direction.DOWN and not has_below:
                    self.direction = Direction.UP if has_above else Direction.IDLE

    def __str__(self) -> str:
        """
        Return a string representation of the elevator's status.
        """
        emergency_str = " [EMERGENCY]" if self.is_emergency else ""
        blocked_str = " [BLOCKED]" if self.is_blocked else ""
        fireman_str = " [FIREMAN MODE]" if self.is_fireman_mode else ""
        requests_list = sorted(list(self.requests))
        return (f"Elevator {self.name} [{self.side}]{emergency_str}{blocked_str}{fireman_str}: "
                f"Floor {self.current_floor}, Direction {self.direction.name}, "
                f"Requests {requests_list}")
