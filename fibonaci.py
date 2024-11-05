# Number of terms to generate in the Fibonacci series
num_terms = 10

# Initialize the first two Fibonacci numbers
a, b = 0, 1

# Print the Fibonacci series
print("Fibonacci Series:")
for _ in range(num_terms):
    print(a, end=' ')  # Print the current Fibonacci number
   
    a,b=b,a+b # Update a and b for the next iteration