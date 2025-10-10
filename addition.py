#!/usr/bin/env python3
"""
Python program for addition of numbers
Demonstrates various ways to add numbers
"""

def add_two_numbers(a, b):
    """Add two numbers and return the result"""
    return a + b

def add_multiple_numbers(*args):
    """Add multiple numbers using variable arguments"""
    return sum(args)

def add_from_list(numbers):
    """Add all numbers in a list"""
    return sum(numbers)

def interactive_addition():
    """Interactive addition program"""
    print("=== Number Addition Program ===")
    print("1. Add two numbers")
    print("2. Add multiple numbers")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = add_two_numbers(num1, num2)
                print(f"Result: {num1} + {num2} = {result}")
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '2':
            try:
                numbers_input = input("Enter numbers separated by spaces: ")
                numbers = [float(x) for x in numbers_input.split()]
                if numbers:
                    result = add_multiple_numbers(*numbers)
                    print(f"Result: {' + '.join(map(str, numbers))} = {result}")
                else:
                    print("No numbers entered!")
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '3':
            print("Thank you for using the addition program!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    # Example usage
    print("Simple Addition Examples:")
    print("-" * 25)
    
    # Add two numbers
    result1 = add_two_numbers(10, 5)
    print(f"10 + 5 = {result1}")
    
    # Add multiple numbers
    result2 = add_multiple_numbers(1, 2, 3, 4, 5)
    print(f"1 + 2 + 3 + 4 + 5 = {result2}")
    
    # Add numbers from a list
    numbers_list = [2.5, 3.7, 1.8, 4.2]
    result3 = add_from_list(numbers_list)
    print(f"Sum of {numbers_list} = {result3}")
    
    print("\n" + "=" * 40)
    
    # Start interactive mode
    interactive_addition()
