# Jess Monnier, CSD-325 Assignment 8.2, 17 February 2025
# This is a program to read from and update a JSON file

# Import needed modules
import json
import os

# Have Python move into this file's working directory
# so that I don't have to do it before running the script
working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)

# Define filename for json records
json_file = 'student.json'

# Function to iterate through records in data & print via dictionary keys
def print_records(data):
    for record in data:
        print(f"{record['L_Name']}, {record['F_Name']} : ", end="")
        print(f"ID = {record['Student_ID']}, Email = {record['Email']}")

# Welcome message
input(f"\nThis program will print the contents of {json_file}. Press Enter to begin...\n")

# Open the file, assign its contents to data variable via json module
with open(json_file, 'r') as f:
    data = json.load(f)

# Send this data to the print_records function
print(f"--- Printing formatted contents of {json_file} ---")
print_records(data)

# Add my info to the data variable
data.append({'F_Name': 'Jess', 'L_Name': 'Monnier', 'Student_ID': '31337',
             'Email': 'jmonnier@my365.bellevue.edu'})

# Notify user the previous step was completed
input("\nNew record added to the list. Please press Enter to print the new list...\n")

# Send updated data to the print_records function
print(f"--- Printing updated contents of {json_file} ---")
print_records(data)

# Have user trigger updating the JSON file
response = input(f"\nTo update {json_file} with this new record, press Enter. To quit instead, enter quit.\n")

# Check if user wanted to update record
if 'quit' in response.lower():
    print('\nQuitting...\n')
else:
    # Write the updated data to the JSON file
    with open(json_file, 'w') as j:
        json.dump(data, j, indent=4, separators=(',', ': '))
    
    # Notify user the update was completed
    input(f"\n{json_file} was updated with the new record. Press Enter to end the program.\n")