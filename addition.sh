#!/bin/bash

# Shell script for addition of numbers
# Demonstrates various ways to add numbers in bash

# Function to add two numbers
add_two_numbers() {
    local num1=$1
    local num2=$2
    echo "scale=2; $num1 + $num2" | bc
}

# Function to add multiple numbers
add_multiple_numbers() {
    local sum=0
    for num in "$@"; do
        sum=$(echo "scale=2; $sum + $num" | bc)
    done
    echo $sum
}

# Function to validate if input is a number
is_number() {
    if [[ $1 =~ ^-?[0-9]+\.?[0-9]*$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function for interactive addition
interactive_addition() {
    echo "=== Number Addition Program (Shell Script) ==="
    echo "1. Add two numbers"
    echo "2. Add multiple numbers"
    echo "3. Add numbers from file"
    echo "4. Exit"
    
    while true; do
        echo
        read -p "Enter your choice (1-4): " choice
        
        case $choice in
            1)
                read -p "Enter first number: " num1
                read -p "Enter second number: " num2
                
                if is_number "$num1" && is_number "$num2"; then
                    result=$(add_two_numbers "$num1" "$num2")
                    echo "Result: $num1 + $num2 = $result"
                else
                    echo "Please enter valid numbers!"
                fi
                ;;
            2)
                read -p "Enter numbers separated by spaces: " -a numbers
                
                # Validate all numbers
                valid=true
                for num in "${numbers[@]}"; do
                    if ! is_number "$num"; then
                        valid=false
                        break
                    fi
                done
                
                if [ "$valid" = true ] && [ ${#numbers[@]} -gt 0 ]; then
                    result=$(add_multiple_numbers "${numbers[@]}")
                    numbers_str=$(IFS=" + "; echo "${numbers[*]}")
                    echo "Result: $numbers_str = $result"
                else
                    echo "Please enter valid numbers!"
                fi
                ;;
            3)
                read -p "Enter filename containing numbers (one per line): " filename
                if [ -f "$filename" ]; then
                    # Read numbers from file and add them
                    numbers_array=()
                    while IFS= read -r line; do
                        # Skip empty lines and comments
                        if [[ -n "$line" && ! "$line" =~ ^# ]]; then
                            if is_number "$line"; then
                                numbers_array+=("$line")
                            else
                                echo "Warning: Skipping invalid number: $line"
                            fi
                        fi
                    done < "$filename"
                    
                    if [ ${#numbers_array[@]} -gt 0 ]; then
                        result=$(add_multiple_numbers "${numbers_array[@]}")
                        echo "Sum of numbers from $filename: $result"
                        echo "Numbers added: ${numbers_array[*]}"
                    else
                        echo "No valid numbers found in file!"
                    fi
                else
                    echo "File not found: $filename"
                fi
                ;;
            4)
                echo "Thank you for using the addition program!"
                break
                ;;
            *)
                echo "Invalid choice! Please enter 1, 2, 3, or 4."
                ;;
        esac
    done
}

# Function to display usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [numbers...]"
    echo
    echo "OPTIONS:"
    echo "  -h, --help       Show this help message"
    echo "  -i, --interactive Run in interactive mode"
    echo "  -f, --file FILE  Add numbers from file"
    echo
    echo "Examples:"
    echo "  $0 10 5                    # Add two numbers: 10 + 5"
    echo "  $0 1 2 3 4 5               # Add multiple numbers"
    echo "  $0 -i                      # Run interactive mode"
    echo "  $0 -f numbers.txt          # Add numbers from file"
    echo "  $0 3.14 2.86 1.5           # Add decimal numbers"
}

# Main execution logic
main() {
    # Check if bc is available (required for decimal arithmetic)
    if ! command -v bc &> /dev/null; then
        echo "Error: 'bc' command is required but not installed."
        echo "Please install bc: sudo apt-get install bc (Ubuntu/Debian)"
        exit 1
    fi
    
    # If no arguments provided, show examples and start interactive mode
    if [ $# -eq 0 ]; then
        echo "Simple Addition Examples:"
        echo "========================"
        
        # Example 1: Add two numbers
        result1=$(add_two_numbers 10 5)
        echo "10 + 5 = $result1"
        
        # Example 2: Add multiple numbers
        result2=$(add_multiple_numbers 1 2 3 4 5)
        echo "1 + 2 + 3 + 4 + 5 = $result2"
        
        # Example 3: Add decimal numbers
        result3=$(add_multiple_numbers 2.5 3.7 1.8 4.2)
        echo "2.5 + 3.7 + 1.8 + 4.2 = $result3"
        
        echo
        echo "========================================"
        echo
        
        # Start interactive mode
        interactive_addition
        return
    fi
    
    # Parse command line arguments
    case $1 in
        -h|--help)
            show_usage
            ;;
        -i|--interactive)
            interactive_addition
            ;;
        -f|--file)
            if [ -z "$2" ]; then
                echo "Error: Please specify a filename"
                show_usage
                exit 1
            fi
            
            filename="$2"
            if [ -f "$filename" ]; then
                numbers_array=()
                while IFS= read -r line; do
                    if [[ -n "$line" && ! "$line" =~ ^# ]]; then
                        if is_number "$line"; then
                            numbers_array+=("$line")
                        else
                            echo "Warning: Skipping invalid number: $line"
                        fi
                    fi
                done < "$filename"
                
                if [ ${#numbers_array[@]} -gt 0 ]; then
                    result=$(add_multiple_numbers "${numbers_array[@]}")
                    echo "Sum of numbers from $filename: $result"
                else
                    echo "No valid numbers found in file!"
                fi
            else
                echo "Error: File not found: $filename"
                exit 1
            fi
            ;;
        *)
            # Validate all arguments are numbers
            for arg in "$@"; do
                if ! is_number "$arg"; then
                    echo "Error: '$arg' is not a valid number"
                    show_usage
                    exit 1
                fi
            done
            
            # Add all provided numbers
            result=$(add_multiple_numbers "$@")
            numbers_str=$(IFS=" + "; echo "$*")
            echo "$numbers_str = $result"
            ;;
    esac
}

# Run main function with all arguments
main "$@"
