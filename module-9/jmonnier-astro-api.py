# Jess Monnier, Assignment 9.2, 18 February 2025
# This is a program to query and then display the list of people in space

import requests as req
from time import sleep

# Print a formatted version of the json result (indentation, new lines, etc)
# def jprint(object):
#     text = json.dumps(object, sort_keys=True, indent=4)
#     print(text)

# Number of seconds to pause (to keep the program easier to follow)
snooze = 1.5

# Welcome message
input("\nPress Enter to see who's in space! This may take a few seconds...\n")

# Request a response from the astros.json API
response = req.get('http://api.open-notify.org/astros.json')

# Check whether the request was successful before running the rest
if response.status_code != 200:
    print("Our API response returned an error. Please try running the script again.\n")

else:

    # Store the json from the response
    data = response.json()

    # Organize the data to make displaying it nicely easier
    space = {}
    for i in data["people"]:
        if space.get(i["craft"]):
            space[i["craft"]].append(i["name"])
        else:
            space[i["craft"]] = [i["name"]]

    # Print summary data
    print(f"Currently, there are {data["number"]} people in space!")
    print(f"They are on {len(space.keys())} different spacecraft: ", end="")
    print(", ".join(space.keys()))
    print()

    # Print astronauts per craft
    for craft in space.keys():
        sleep(snooze)
        print(f"Crew of the {craft}: {len(space[craft])}")
        # Only print 4 names per line to prevent long lines
        left = 0
        right = min(4, len(space[craft]))
        while len(space[craft]) > right:
            print(", ".join(space[craft][left:right]) + ",")
            left += 4
            right += 4
        if left <= len(space[craft]): # Print remaining names, if any
            print(", ".join(space[craft][left:len(space[craft])+1]))
        print()
        sleep(snooze)

    # Exit message
    input("And that's it for now! Press Enter to quit...\n")