"""
Unit tests for basic elevator movement and system logic.
"""
import sys
import os
import unittest
import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elevator import Elevator, Direction
from elevator_system import ElevatorSystem


class TestElevator(unittest.TestCase):
    """
    Test suite for basic elevator and elevator system functionality.
    """

    def test_elevator_independence(self) -> None:
        """Test that elevators operate independently."""
        e1 = Elevator('A', 'North')
        e2 = Elevator('B', 'North')

        e1.add_request(5)
        e2.add_request(2)

        for _ in range(2):
            e1.move()
            e2.move()

        self.assertEqual(e1.current_floor, 2)
        self.assertEqual(e2.current_floor, 2)
        self.assertEqual(e2.direction, Direction.IDLE)  # Arrived and cleared

        e1.move()
        self.assertEqual(e1.current_floor, 3)

    def test_system_initialization(self) -> None:
        """Test that the system initializes with correct elevator configuration."""
        system = ElevatorSystem()
        self.assertEqual(len(system.elevators), 6)
        self.assertEqual(system.elevators['A'].side, 'North')
        self.assertEqual(system.elevators['D'].side, 'South')

    def test_side_assignment(self) -> None:
        """Test that requests are assigned to elevators on the correct side."""
        system = ElevatorSystem()
        # All start at floor 0
        system.request_elevator(5, side='South')
        # Should be assigned to D, E, or F
        assigned = [e.name for e in system.elevators.values() if 5 in e.requests]
        self.assertTrue(any(name in ['D', 'E', 'F'] for name in assigned))
        self.assertFalse(any(name in ['A', 'B', 'C'] for name in assigned))

    def test_busy_hours(self) -> None:
        """Test busy hour detection logic."""
        system = ElevatorSystem()

        # Test 8:30 AM (Busy)
        self.assertTrue(system.is_busy_hour(datetime.time(8, 30)))

        # Test 10:00 AM (Not Busy)
        self.assertFalse(system.is_busy_hour(datetime.time(10, 0)))

        # Test 12:00 PM (Busy)
        self.assertTrue(system.is_busy_hour(datetime.time(12, 0)))

        # Test 5:00 AM (Busy)
        self.assertTrue(system.is_busy_hour(datetime.time(5, 0)))

        # Test 5:00 PM (Not Busy)
        self.assertFalse(system.is_busy_hour(datetime.time(17, 0)))


if __name__ == '__main__':
    unittest.main()
