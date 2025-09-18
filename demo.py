#!/usr/bin/env python3
"""
Simple demo script that uses the calculator module.
"""

from calculator import add, subtract, multiply, divide, power


def main():
    """Demonstrate calculator functionality."""
    print("Calculator Demo")
    print("=" * 15)
    
    # Basic arithmetic operations
    a, b = 10, 3
    
    print(f"Numbers: {a} and {b}")
    print(f"Addition: {a} + {b} = {add(a, b)}")
    print(f"Subtraction: {a} - {b} = {subtract(a, b)}")
    print(f"Multiplication: {a} * {b} = {multiply(a, b)}")
    print(f"Division: {a} / {b} = {divide(a, b):.2f}")
    print(f"Power: {a} ^ {b} = {power(a, b)}")
    
    # Test with floating point numbers
    print("\nFloating point operations:")
    x, y = 7.5, 2.5
    print(f"Numbers: {x} and {y}")
    print(f"Addition: {x} + {y} = {add(x, y)}")
    print(f"Division: {x} / {y} = {divide(x, y)}")
    
    # Demonstrate error handling
    print("\nError handling:")
    try:
        result = divide(5, 0)
        print(f"5 / 0 = {result}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()