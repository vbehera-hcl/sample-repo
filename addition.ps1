# PowerShell script for addition of numbers
# Demonstrates various ways to add numbers in PowerShell

# Function to validate if input is a number
function Test-IsNumber {
    param([string]$Value)
    
    try {
        [double]$Value | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to add two numbers
function Add-TwoNumbers {
    param(
        [double]$Num1,
        [double]$Num2
    )
    return $Num1 + $Num2
}

# Function to add multiple numbers
function Add-MultipleNumbers {
    param([double[]]$Numbers)
    
    $sum = 0
    foreach ($num in $Numbers) {
        $sum += $num
    }
    return $sum
}

# Function for interactive addition
function Start-InteractiveAddition {
    Write-Host "=== Number Addition Program (PowerShell) ===" -ForegroundColor Cyan
    Write-Host "1. Add two numbers"
    Write-Host "2. Add multiple numbers" 
    Write-Host "3. Add numbers from file"
    Write-Host "4. Exit"
    
    do {
        Write-Host ""
        $choice = Read-Host "Enter your choice (1-4)"
        
        switch ($choice) {
            "1" {
                $num1Str = Read-Host "Enter first number"
                $num2Str = Read-Host "Enter second number"
                
                if ((Test-IsNumber $num1Str) -and (Test-IsNumber $num2Str)) {
                    $num1 = [double]$num1Str
                    $num2 = [double]$num2Str
                    $result = Add-TwoNumbers $num1 $num2
                    Write-Host "Result: $num1 + $num2 = $result" -ForegroundColor Green
                }
                else {
                    Write-Host "Please enter valid numbers!" -ForegroundColor Red
                }
            }
            "2" {
                $numbersInput = Read-Host "Enter numbers separated by spaces"
                $numberStrings = $numbersInput -split '\s+'
                
                $validNumbers = @()
                $allValid = $true
                
                foreach ($numStr in $numberStrings) {
                    if ($numStr -ne "" -and (Test-IsNumber $numStr)) {
                        $validNumbers += [double]$numStr
                    }
                    elseif ($numStr -ne "") {
                        $allValid = $false
                        break
                    }
                }
                
                if ($allValid -and $validNumbers.Count -gt 0) {
                    $result = Add-MultipleNumbers $validNumbers
                    $numbersStr = $validNumbers -join " + "
                    Write-Host "Result: $numbersStr = $result" -ForegroundColor Green
                }
                else {
                    Write-Host "Please enter valid numbers!" -ForegroundColor Red
                }
            }
            "3" {
                $filename = Read-Host "Enter filename containing numbers (one per line)"
                
                if (Test-Path $filename) {
                    $numbers = @()
                    $lines = Get-Content $filename
                    
                    foreach ($line in $lines) {
                        $trimmedLine = $line.Trim()
                        # Skip empty lines and comments
                        if ($trimmedLine -ne "" -and !$trimmedLine.StartsWith("#")) {
                            if (Test-IsNumber $trimmedLine) {
                                $numbers += [double]$trimmedLine
                            }
                            else {
                                Write-Host "Warning: Skipping invalid number: $trimmedLine" -ForegroundColor Yellow
                            }
                        }
                    }
                    
                    if ($numbers.Count -gt 0) {
                        $result = Add-MultipleNumbers $numbers
                        Write-Host "Sum of numbers from $filename`: $result" -ForegroundColor Green
                        Write-Host "Numbers added: $($numbers -join ', ')" -ForegroundColor Cyan
                    }
                    else {
                        Write-Host "No valid numbers found in file!" -ForegroundColor Red
                    }
                }
                else {
                    Write-Host "File not found: $filename" -ForegroundColor Red
                }
            }
            "4" {
                Write-Host "Thank you for using the addition program!" -ForegroundColor Cyan
                return
            }
            default {
                Write-Host "Invalid choice! Please enter 1, 2, 3, or 4." -ForegroundColor Red
            }
        }
    } while ($true)
}

# Function to show usage
function Show-Usage {
    Write-Host "Usage: .\addition.ps1 [OPTIONS] [numbers...]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "OPTIONS:"
    Write-Host "  -Help            Show this help message"
    Write-Host "  -Interactive     Run in interactive mode"  
    Write-Host "  -File <FILE>     Add numbers from file"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\addition.ps1 10 5                    # Add two numbers: 10 + 5"
    Write-Host "  .\addition.ps1 1 2 3 4 5               # Add multiple numbers"
    Write-Host "  .\addition.ps1 -Interactive            # Run interactive mode"
    Write-Host "  .\addition.ps1 -File numbers.txt       # Add numbers from file"
    Write-Host "  .\addition.ps1 3.14 2.86 1.5           # Add decimal numbers"
}

# Main execution logic
param(
    [switch]$Help,
    [switch]$Interactive,
    [string]$File,
    [string[]]$Numbers = $args
)

# Handle help
if ($Help) {
    Show-Usage
    return
}

# Handle interactive mode
if ($Interactive) {
    Start-InteractiveAddition
    return
}

# Handle file input
if ($File) {
    if (Test-Path $File) {
        $numbers = @()
        $lines = Get-Content $File
        
        foreach ($line in $lines) {
            $trimmedLine = $line.Trim()
            # Skip empty lines and comments
            if ($trimmedLine -ne "" -and !$trimmedLine.StartsWith("#")) {
                if (Test-IsNumber $trimmedLine) {
                    $numbers += [double]$trimmedLine
                }
                else {
                    Write-Host "Warning: Skipping invalid number: $trimmedLine" -ForegroundColor Yellow
                }
            }
        }
        
        if ($numbers.Count -gt 0) {
            $result = Add-MultipleNumbers $numbers
            Write-Host "Sum of numbers from $File`: $result" -ForegroundColor Green
        }
        else {
            Write-Host "No valid numbers found in file!" -ForegroundColor Red
        }
    }
    else {
        Write-Host "Error: File not found: $File" -ForegroundColor Red
        exit 1
    }
    return
}

# If no specific parameters and no numbers provided, show examples and start interactive
if ($Numbers.Count -eq 0) {
    Write-Host "Simple Addition Examples:" -ForegroundColor Cyan
    Write-Host "========================"
    
    # Example 1: Add two numbers
    $result1 = Add-TwoNumbers 10 5
    Write-Host "10 + 5 = $result1"
    
    # Example 2: Add multiple numbers
    $result2 = Add-MultipleNumbers @(1, 2, 3, 4, 5)
    Write-Host "1 + 2 + 3 + 4 + 5 = $result2"
    
    # Example 3: Add decimal numbers
    $result3 = Add-MultipleNumbers @(2.5, 3.7, 1.8, 4.2)
    Write-Host "2.5 + 3.7 + 1.8 + 4.2 = $result3"
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Start interactive mode
    Start-InteractiveAddition
}
else {
    # Validate all arguments are numbers
    $validNumbers = @()
    $allValid = $true
    
    foreach ($num in $Numbers) {
        if (Test-IsNumber $num) {
            $validNumbers += [double]$num
        }
        else {
            Write-Host "Error: '$num' is not a valid number" -ForegroundColor Red
            $allValid = $false
        }
    }
    
    if ($allValid) {
        # Add all provided numbers
        $result = Add-MultipleNumbers $validNumbers
        $numbersStr = $validNumbers -join " + "
        Write-Host "$numbersStr = $result" -ForegroundColor Green
    }
    else {
        Show-Usage
        exit 1
    }
}
