"""
Henry Gardner, hgardne4@u.rochester.edu 
Mashey Techincal Interview Project

Details on the project and code can be seen below and in the README.txt
"""
import json
import requests

#API Key associated with my NASA API account
NASA_API_KEY = '6aGRFDDOVzBiRf032kKyBbHRhOempO7kgnjHBcZy'
link = 'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=' + NASA_API_KEY 

"""
Function that prints out the json data returned by the NASA API with only the closest approach returned.
Notes:
	* from first inspection, the 'close_approach_date' field is a string not a date
		- would normally have to convert to some numerical type and compare values, but they are already in increasing order
		- therefore, just set the 'close_approach_data' section to contain only the first approach in the list
"""
def asteroid_closest_approach():
	# using the requests library, call the NASA API 
	response = requests.get(link)
	response = response.json()
	# the current response has the following keys (json is a dictionary): links, page, near_earth_objects
	# update such that the response is just the near earth objects, and update the 'close_approach_data' field
	response = response['near_earth_objects']

	file = open('outputs/asteroid_closest_approach_OUTPUT.txt', 'w')
	# loop through the limit of the response
	for i in range(len(response)):
		# update the 'close_approach_data' to contain only the first element and print/add contents to output file
		response[i]['close_approach_data'] = response[i]['close_approach_data'][0]
		print("ASTEROID NUMER: " + str(i+1))
		file.write('{}\n{}\n\n'.format("ASTEROID NUMER: " + str(i+1), json.dumps(response[i], indent=2)))
		print(json.dumps(response[i], indent=2) + "\n")
	file.close()
	
"""
Function that returns the closest asteroid approaches between two dates
Inputs:
	start_date -> the value associated with the beginning of the search
	end_date   -> the value associated with the end of the search
"""
def month_closest_approaches(start_date, end_date):
	date_link = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start_date + '&end_date=' + end_date 

# "main" method, where the program begins
if __name__ == '__main__':
	print("{}\n{}\n{}\n\n".format("Henry Gardner, hgardne4@u.rochester.edu", "Mashey Asteroid Hunter Technical Interview", "October 15, 2021"))
	print("This project creates a data pipeline to track asteroids based on certain criteria.")
	print("Refer to the outputs folder which contains the output from these functions.")
	print("{}\n\t{}\n\t{}\n\t{}".format("Functions to test", "1. asteroid_closest_approach()", "2. month_closest_approaches()", "3. nearest_misses()"))
	user_input = input("Enter a number to test a corresponding function (i.e. '1' for testing asteroid_closest_approach()): ")
	if int(user_input) == 1:
		print("Testing the asteroid_closest_approach() function: \n")
		asteroid_closest_approach()
		print("Completed the asteroid_closest_approach() function, scroll to top for full output.")
	elif int(user_input) == 2:
		print("")
	elif int(user_input) == 3:
		print('')
	else:
		print("Unrecognized input, please enter a number between 1 and 3.")



