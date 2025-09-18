# Test Calculator

A simple calculator implementation with comprehensive unit tests.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide, power)
- Error handling for edge cases (e.g., division by zero)
- Comprehensive unit tests
- Demo script to showcase functionality

## Files

- `calculator.py` - Main calculator module with arithmetic functions
- `test_calculator.py` - Unit tests for all calculator functions
- `demo.py` - Demo script showcasing calculator usage

## Usage

### Running the Demo
```bash
python3 demo.py
```

### Running Tests
```bash
python3 -m unittest test_calculator.py -v
```

### Using the Calculator Module
```python
from calculator import add, subtract, multiply, divide, power

result = add(5, 3)  # Returns 8
result = divide(10, 2)  # Returns 5.0
```

## Testing

The repository includes comprehensive unit tests that cover:
- All basic arithmetic operations
- Edge cases (zero values, negative numbers)
- Error conditions (division by zero)
- Floating point operations

All tests can be run using Python's built-in unittest framework.
