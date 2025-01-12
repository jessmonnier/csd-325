# Jessica Monnier, Module 3.2 Assignment, 29 October 2024
# This is a program to take user input and perform the classic bottles of beer on the wall song

# Import sleep from time for aesthetic purposes
from time import sleep

# Initial variables
pause = 0.7
count = 0

# Welcome message
print()
print("How many bottles of beer are on the wall?")
sleep(pause)
print("Enter a whole number bigger than 0 to begin, or q to quit.")

# Create the function to count bottles of beer
def bottles(n):
    
    # Loop until we run out of beer
    while n > 0:
        sleep(pause)
        print()

        # Check for multiple bottles of beer:
        if n > 1:
            print(f"{n} bottles of beer on the wall, {n} bottles of beer.")
        else:
            print("1 bottle of beer on the wall, 1 bottle of beer.")
        
        # Decrement n
        n -= 1
        
        # Check for 1 bottle of beer:
        sleep(pause)
        if n == 1:
            print("Take one down and pass it around, 1 bottle of beer on the wall.")
        else:
            print(f"Take one down and pass it around, {n} bottles of beer on the wall.")
        
        sleep(pause)

# Loop for input validation purposes
while count <= 0:
    
    # Take user input
    response = input("> ")

    # Check for q:
    if "q" in response.lower():
        break

    # Check for integer input:
    try:
        count = int(response)
    except ValueError:
        pass

    # Check for positive integer:
    if count > 0:
        bottles(count)

        # Print the reminder to get more beer
        sleep(pause)
        print()
        print("Seems like it's time to buy more beer! Thanks for playing!")
        break
    else:
        print()
        print("Your input was invalid. Please input a whole number greater than zero, or q to quit.")

sleep(pause)
print()
print("Goodbye for now :)")
print()