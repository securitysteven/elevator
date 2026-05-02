"""
Unit tests to fill remaining coverage gaps.
"""
import sys
import os
import unittest
import datetime
from io import StringIO

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elevator import Elevator, Direction
from elevator_system import ElevatorSystem

class TestCoverage(unittest.TestCase):
    """
    Tests specifically targeting uncovered branches in the codebase.
    """

    def test_elevator_str(self) -> None:
        """Test the __str__ method of Elevator with various states."""
        e = Elevator('T', 'Test', is_emergency=True)
        e.is_blocked = True
        e.is_fireman_mode = True
        e.requests.add(5)
        s = str(e)
        self.assertIn('[EMERGENCY]', s)
        self.assertIn('[BLOCKED]', s)
        self.assertIn('[FIREMAN MODE]', s)
        self.assertIn('Requests [5]', s)

    def test_elevator_move_idle_and_down(self) -> None:
        """Test movement branches: idle when no requests, and switching to down."""
        e = Elevator('A', 'North')
        # Coverage for 68-69 (idle when no requests)
        e.move()
        self.assertEqual(e.direction, Direction.IDLE)
        
        # Coverage for 89-90 (switching from DOWN to UP if has_above)
        e.current_floor = 5
        e.add_request(4)
        e.add_request(6)
        self.assertEqual(e.direction, Direction.DOWN)
        e.move() # Move to 4
        # At 4, should have 6 above. direction should switch to UP.
        self.assertEqual(e.current_floor, 4)
        self.assertEqual(e.direction, Direction.UP)

    def test_elevator_add_request_blocked_msg(self) -> None:
        """Test the message when adding request to a blocked elevator."""
        e = Elevator('B', 'North')
        e.is_blocked = True
        captured_output = StringIO()
        sys.stdout = captured_output
        result = e.add_request(5)
        sys.stdout = sys.__stdout__
        self.assertFalse(result)
        self.assertIn("is blocked due to fire drill", captured_output.getvalue())

    def test_elevator_system_fireman_override_errors(self) -> None:
        """Test error conditions for fireman_override."""
        system = ElevatorSystem()
        
        # 62-63: Fire drill not active
        captured_output = StringIO()
        sys.stdout = captured_output
        system.fireman_override('A', 5)
        sys.stdout = sys.__stdout__
        self.assertIn("Fire drill is not active", captured_output.getvalue())
        
        # 71: Elevator not found
        system.activate_fire_drill()
        captured_output = StringIO()
        sys.stdout = captured_output
        system.fireman_override('Z', 5)
        sys.stdout = sys.__stdout__
        self.assertIn("Elevator Z not found", captured_output.getvalue())

    def test_elevator_system_is_busy_hour_default(self) -> None:
        """Test is_busy_hour with default current_time (84)."""
        system = ElevatorSystem()
        # Just call it to ensure line 84 is covered. Result depends on system clock.
        system.is_busy_hour()

    def test_elevator_system_request_fallback(self) -> None:
        """Test fallback to emergency elevators for normal requests (109)."""
        system = ElevatorSystem()
        # Set all non-emergency elevators to a different floor to distinguish
        for name in ['A', 'B', 'D', 'E']:
            system.elevators[name].current_floor = 10
            
        # We want filter_elevators(False) to return empty list.
        # But filter_elevators(False) returns A, B, D, E regardless of blocked status.
        # It's based on e.is_emergency.
        
        # To make 'eligible' empty in line 105 for a normal request (is_priority=False):
        # We need filter_elevators(False) to be empty.
        # This happens if we use a 'side' that has no non-emergency elevators.
        # But all sides (North, South) have non-emergency elevators.
        
        # Let's temporarily change an elevator's side or emergency status to test this branch.
        system.elevators['A'].is_emergency = True
        system.elevators['B'].is_emergency = True
        # Now North side has only emergency elevators (A, B, C).
        
        captured_output = StringIO()
        sys.stdout = captured_output
        system.request_elevator(5, side='North')
        sys.stdout = sys.__stdout__
        
        # Should have fallen back to emergency elevators on North side.
        assigned = [e.name for e in system.elevators.values() if 5 in e.requests]
        self.assertTrue(any(name in ['A', 'B', 'C'] for name in assigned))

    def test_elevator_system_status(self) -> None:
        """Test the status() method of ElevatorSystem."""
        system = ElevatorSystem()
        captured_output = StringIO()
        sys.stdout = captured_output
        system.status()
        sys.stdout = sys.__stdout__
        self.assertIn("Elevator A", captured_output.getvalue())
        self.assertIn("Elevator F", captured_output.getvalue())

    def test_elevator_add_request_idle_logic(self) -> None:
        """Test add_request logic for setting direction when idle (56)."""
        e = Elevator('A', 'North')
        e.current_floor = 5
        e.add_request(5)
        self.assertEqual(e.direction, Direction.IDLE)

    def test_elevator_move_arrival_logic(self) -> None:
        """Test more complex arrival/direction switching logic (73-74, 87-88)."""
        e = Elevator('A', 'North')
        # UP to DOWN (87-88)
        e.current_floor = 2
        e.add_request(3)
        e.add_request(1)
        self.assertEqual(e.direction, Direction.UP)
        e.move() # to 3
        self.assertEqual(e.current_floor, 3)
        self.assertEqual(e.direction, Direction.DOWN)
        
        # Arrival logic: 73-74 (Down movement)
        e.move() # to 2
        e.move() # to 1
        self.assertEqual(e.current_floor, 1)
        self.assertEqual(e.direction, Direction.IDLE)

if __name__ == '__main__':
    unittest.main()
