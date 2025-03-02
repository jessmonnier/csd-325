# Jess Monnier, Assignment 9.2, 18 February 2025
# This is a program to search for a Star Wars character via the Star Wars API

import requests as req

# Print a formatted version of the json result (indentation, new lines, etc)
# def jprint(object):
#     text = json.dumps(object, indent=4)
#     print(text)

# Welcome message
print("\nThis will allow you to search for a character on the Star Wars API.")
input("First, let's check that the API is working. Press Enter to check...\n")

# Turn the api URL into a variable so we can change it as needed
api = 'https://swapi.dev/api/people'
response = req.get(api)

# Check to make sure API is up and running. (Curse the Futurama API for trolling me.)
if response.status_code != 200:
    print("The API returned an error code. You may want to try running the script again.\n")

# If it's running, execute the script.
else:
    print("The API is up! Please enter all or part of the name of a Star Wars ")
    print("character to search for. The script will return the first match it finds.")
    print("This may take a little while!")

    # Store user input as string in lowercase to help with consistent results.
    search = input("> ").lower()

    # Initial values for character and err are None to help track success/failure.
    character = None
    err = None

    # While loop to search pages of characters until we run out (manual break)
    while True:

        # Set data within the while loop; use initial query first & at end of loop
        # set response to result of next query.
        data = response.json()

        # Search each character in the results, break if there's a match
        for result in data['results']:
            if search in result['name'].lower():
                character = result # put character's dictionary in character variable
                break
        
        # Once the loop ends, check to see if character now has data
        if character:
            break
        
        # The response json includes the API url for the next page, so if that's populated,
        # use it to perform the next query
        if data['next']:
            api = data['next']

            # Give the user a status update
            print(f"\nNo results found on page {int(api.split("=")[1])-1}. Querying next page.")

            # Next query
            response = req.get(api)

            # Check that it was successful, break if not
            if response.status_code != 200:
                err = response.status_code
                break
        # If there are no more pages, we want to break the loop so it's not infinite
        else: 
            break

    # If search was successful, print some of the character info found.
    if character:
        print(f"\nResult! Your search for '{search}' found {character["name"]}.")
        print(f"Height: {character["height"]}cm".ljust(20), end="")
        print(f"Mass: {character["mass"]}kg".ljust(20), end="")
        print(f"Birth Year: {character["birth_year"]}")
        print(f"Gender: {character["gender"]}".ljust(20), end="")
        print(f"Hair: {character["hair_color"]}".ljust(20), end="")
        print(f"Eyes: {character["eye_color"]}")
        
        # Goodbye
        input("\nSearch complete! Press Enter to exit...\n")
    
    # If there was an error from API, print the page on which it occurred and exit.
    elif err:
        print(f"\nThe API returned error code {err} retrieving page {api.split("=")[1]}.")
        print("Exiting...\n")
    
    # If we made it this far, no result was found but all pages were queried.
    # Update user and exit.
    else:
        print(f"\nYour search for '{search}' returned no results.")
        print("Exiting...\n")