# Example code with some technical debt
import os

# TODO: Add proper error handling
def process_data(data):
    password = "hardcoded123"  # Security issue
    result = eval(data)  # Dangerous!
    
    for i in range(10):
        for j in range(10):  # Nested loop
            print(i * j)
    
    return result

if __name__ == "__main__":
    process_data("2+2")
