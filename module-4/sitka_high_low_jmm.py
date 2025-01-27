# Jessica Monnier, Module 4.2 Assignment, 26 January 2025
# This is a revision to the sitka_highs.py program provided for class
# The original program plotted daily highs from a csv file using matplotlib
# Comments from the original program are prefaced with "Original comment:"

import csv
from datetime import datetime
from matplotlib import pyplot as plt
# Sleep will be used to keep the terminal readable
from time import sleep
# Sys will be used to fully exit the program in the event of nested loops
import sys

# Set value (in seconds) to use for sleep
lil_pause = 0.8

# Adding welcome message with instructions for user
print('''
Welcome to the daily highs and lows plotter.
At the input, please enter one of the options below:
highs - Will plot the daily high temperatures in the data file.
lows - Will plot the daily low temperatures in the data file.
quit - Ends the program.
''')

# Create a while loop to let user to continue until they input quit
while True:

    # Create a while loop for input validation of user response
    while True:
        response = input("> ").lower()
        if len(response) == 0 or response[0] not in 'hlq':
            print()
            print("Your response was not valid. Please enter highs, lows, or quit (h, l, or q).")
            sleep(lil_pause)
            continue
        elif response[0] == 'q':
            print()
            print("Thanks for stopping by!")
            print()
            sys.exit()
        elif response[0] == 'h':
            # Set variables to get/display highs
            rownum = 5
            color = "red"
            title = "Daily high temperatures - 2018"
            break
        else:
            # Set variables to get/display lows
            rownum = 6
            color = "blue"
            title = "Daily low temperatures - 2018"
            break

    filename = 'sitka_weather_2018_simple.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        # Original comment: Get dates and high temperatures from this file.
        # Modified comment: Changed variable names from high/highs to temp/temps for clarity
        dates, temps = [], []
        for row in reader:
            current_date = datetime.strptime(row[2], '%Y-%m-%d')
            dates.append(current_date)
            # Set row index to rownum variable to account for user choice
            temp = int(row[rownum])
            temps.append(temp)

    # Original comment: Plot the high temperatures.
    # Original comment: plt.style.use('seaborn')
    # Modified comment: Set c to the color variable to account for user choice
    fig, ax = plt.subplots()
    ax.plot(dates, temps, c=color)

    # Original comment: Format plot.
    # Modified comment: Set title text to title variable to account for user choice
    plt.title(title, fontsize=24)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel("Temperature (F)", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)

    plt.show()

    # Add a bit of text to prompt the user what happens next once they close plot window
    sleep(lil_pause)
    print()
    print("You closed the plot window! If you'd like to open a new one,")
    print("enter highs or lows. Otherwise, enter quit.")