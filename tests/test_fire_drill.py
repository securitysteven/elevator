"""
Unit tests for fire drill functionality.
"""
import sys
import os
import unittest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from elevator_system import ElevatorSystem


class TestFireDrill(unittest.TestCase):
    """
    Test suite for fire drill blocking and override logic.
    """

    def test_fire_drill_blocking(self) -> None:
        """Test that elevators are blocked and sent to floor 0 during fire drill."""
        system = ElevatorSystem()

        # Initially elevators are not blocked
        self.assertFalse(system.fire_drill_active)
        for e in system.elevators.values():
            self.assertFalse(e.is_blocked)

        # Activate fire drill
        system.activate_fire_drill()
        self.assertTrue(system.fire_drill_active)
        for e in system.elevators.values():
            self.assertTrue(e.is_blocked)
            self.assertIn(0, e.requests)  # All sent to floor 0

        # Requests should be ignored during fire drill
        system.request_elevator(5)
        for e in system.elevators.values():
            if e.current_floor != 5:
                self.assertNotIn(5, e.requests)

    def test_fireman_override(self) -> None:
        """Test that firemen can override blocked elevators."""
        system = ElevatorSystem()
        system.activate_fire_drill()

        # Fireman overrides elevator A to go to floor 8
        system.fireman_override('A', 8)
        self.assertTrue(system.elevators['A'].is_fireman_mode)
        self.assertIn(8, system.elevators['A'].requests)

        # Move elevator A
        for _ in range(8):
            system.step()

        self.assertEqual(system.elevators['A'].current_floor, 8)
        self.assertNotIn(8, system.elevators['A'].requests)

    def test_deactivate_fire_drill(self) -> None:
        """Test that deactivating fire drill restores normal operation."""
        system = ElevatorSystem()
        system.activate_fire_drill()
        system.fireman_override('A', 8)

        system.deactivate_fire_drill()
        self.assertFalse(system.fire_drill_active)
        for e in system.elevators.values():
            self.assertFalse(e.is_blocked)
            self.assertFalse(e.is_fireman_mode)

        # Requests should work again
        system.request_elevator(3)
        assigned = [e.name for e in system.elevators.values() if 3 in e.requests]
        self.assertTrue(len(assigned) > 0)


if __name__ == '__main__':
    unittest.main()
