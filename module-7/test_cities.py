# Jess Monnier, CSD325 Assignment 7.2, 16 February 2025
# This program is designed to test the functionality of other functions.

import unittest
from city_functions import city_info

# create a test case to test the city_info function in city_functions.py
class TestMyFunction(unittest.TestCase):
    def test_city_country(self):
        self.assertEqual(city_info("new york", "united states"), "New York, United States")

# ensure it will run if called on the command line
if __name__ == '__main__':
    unittest.main()