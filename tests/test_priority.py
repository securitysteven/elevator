"""
Unit tests for priority/emergency elevator functionality.
"""
import sys
import os
import unittest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elevator_system import ElevatorSystem


class TestPriorityElevator(unittest.TestCase):
    """
    Test suite for priority and emergency elevator request handling.
    """

    def test_priority_assignment(self) -> None:
        """Test that priority requests are assigned to emergency elevators."""
        system = ElevatorSystem()

        # Priority request should go to C or F
        system.request_elevator(5, is_priority=True)
        assigned = [e.name for e in system.elevators.values() if 5 in e.requests]
        self.assertTrue(all(name in ['C', 'F'] for name in assigned))
        self.assertTrue(len(assigned) > 0)

    def test_normal_avoids_emergency(self) -> None:
        """Test that normal requests prefer non-emergency elevators."""
        system = ElevatorSystem()

        # Normal request should go to A, B, D, or E
        system.request_elevator(3)
        assigned = [e.name for e in system.elevators.values() if 3 in e.requests]
        self.assertTrue(all(name in ['A', 'B', 'D', 'E'] for name in assigned))
        self.assertTrue(len(assigned) > 0)

    def test_priority_with_side(self) -> None:
        """Test priority requests with side preference."""
        system = ElevatorSystem()

        # Priority request North should go to C
        system.request_elevator(7, side='North', is_priority=True)
        assigned = [e.name for e in system.elevators.values() if 7 in e.requests]
        self.assertEqual(assigned, ['C'])

        # Priority request South should go to F
        system.request_elevator(8, side='South', is_priority=True)
        assigned = [e.name for e in system.elevators.values() if 8 in e.requests]
        self.assertEqual(assigned, ['F'])


if __name__ == '__main__':
    unittest.main()
