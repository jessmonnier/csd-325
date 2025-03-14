# Jess Monnier, CSD325 Assignment 7.2, 16 February 2025
# This program defines a function for printing info about a city

# final function has two mandatory parameters & two optional
def city_info(city, country, population = None, language = None):
    
    # create the string generated by the mandatory parameters
    # .title() used to ensure consistent capitalization
    result = f"{city.title()}, {country.title()}"

    # if the population parameter was passed and is an integer, 
    # append that info to the string & format nicely
    if isinstance(population, int):
        result += f" - population {population:,d}"
    
    # if the language parameter was passed, append it to the string
    if language:
        result += f", {language.title()}"
    
    # return the final string
    return result

# First set of calls
print(city_info("Santiago", "Chile"))
print(city_info("Seoul", "south korea"))
print(city_info("vancouver", "canada"))

# Additional later calls
print(city_info("santiago", "Chile", 5000000))
print(city_info("little rock", "arkansas", 203842, "english"))
print(city_info("PARIS", "FRANCE", language="French"))