# Simple Python script to add two numbers

def add_two_numbers():
    print("--- Add Two Numbers ---")
    
    try:
        # Get input from user
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        # Calculate sum
        result = num1 + num2
        
        # Display result
        print(f"The sum of {num1} and {num2} is: {result}")
        
    except ValueError:
        print("Invalid input! Please enter numbers only.")

if __name__ == "__main__":
    add_two_numbers()
