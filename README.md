# Elevator Simulation System

A Python-based simulation of an elevator system in a building with multiple elevators, featuring advanced dispatching logic, busy hour detection, and emergency protocols.

## Features

- **Multiple Elevators**: Manages a fleet of 6 elevators (labeled A-F) distributed across North and South sides of the building.
- **Smart Dispatching**: Assigns requests to the nearest available elevator based on location and current direction.
- **Busy Hour Logic**: Identifies peak times (e.g., morning rush, lunch) where the system behavior might be adjusted.
- **Fire Drill Protocol**: 
    - Emergency mode that sends all elevators to the ground floor.
    - Blocked operation for safety.
    - Fireman override capability to take manual control of an elevator during a drill.
- **Priority Requests**: Dedicated emergency/priority elevators (C and F) for VIP or urgent requests.
- **Hallway Sides**: Requests can be filtered by 'North' or 'South' side of the hallway.

## Project Structure

- `elevator.py`: Contains the `Elevator` class representing individual elevator units.
- `elevator_system.py`: Contains the `ElevatorSystem` class that manages the fleet and dispatch logic.
- `main.py`: Entry point for a basic simulation run.
- `demo/`: Contains specialized simulation scenarios:
    - `demo_busy_hour.py`: Simulates operation during peak traffic.
    - `demo_fire_drill.py`: Demonstrates fire drill activation and fireman override.
- `tests/`: Comprehensive test suite covering various edge cases and features.

## Getting Started

### Prerequisites

- Python 3.6 or higher.

### Running the Simulation

To run the basic simulation:

```bash
python main.py
```

To run specific demo scenarios:

```bash
python demo/demo_busy_hour.py
python demo/demo_fire_drill.py
```

### Running Tests

The project uses `unittest` for testing. To run all tests:

```bash
python -m unittest discover tests
```

## License

This project is released under the [Unlicense](LICENSE), dedicating it to the public domain.
