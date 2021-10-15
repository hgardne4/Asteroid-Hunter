"""
Henry Gardner, hgardne4@u.rochester.edu 
Mashey Techincal Interview Project

Details on the project and code can be seen below and in the README.txt
"""
import json
import requests

# EXCEPTION HANDLING
class RequestException(Exception):
	pass

class DateException(Exception):
	pass

class UserInputException(Exception):
	pass

#API Key associated with my NASA API account
NASA_API_KEY = '6aGRFDDOVzBiRf032kKyBbHRhOempO7kgnjHBcZy'
link = 'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=' + NASA_API_KEY 

"""
Function that prints out the json data returned by the NASA API with only the closest approach returned.
- From first inspection, the 'close_approach_date' field is a string not a date
	- would normally have to convert to some numerical type and compare values, but they are already in increasing order
	- therefore, just set the 'close_approach_data' section to contain only the first approach in the list
"""
def asteroid_closest_approach():
	# using the requests library, call the NASA API 
	response = requests.get(link)
	# check to make sure the response was valid 
	STATUS_CODE = response.status_code
	if STATUS_CODE == 200:
		response = response.json()
		# the current response has the following keys (json is a dictionary): links, page, near_earth_objects
		# update such that the response is just the near earth objects, and update the 'close_approach_data' field
		response = response['near_earth_objects']
		
		file = open('src/outputs/asteroid_closest_approach_OUTPUT.txt', 'w')
		# loop through the limit of the response
		for i in range(len(response)):
			# update the 'close_approach_data' to contain only the first element and print/add contents to output file
			response[i]['close_approach_data'] = response[i]['close_approach_data'][0]
			# print and write to the output file, the output of the response
			print("ASTEROID NUMER: " + str(i+1))
			file.write('{}\n{}\n\n'.format("ASTEROID NUMER: " + str(i+1), json.dumps(response[i], indent=2)))
			print(json.dumps(response[i], indent=2) + "\n")
		file.close()
	# o/w throw exception
	else:
		raise RequestException('Error in requesting data from ' + link + 'in asteroid_closest_approach() function...')


"""
Function that returns the closest asteroid approaches between two dates.
- Note that the NASA API already deals with the situation when the start date is after the end date
- Additionally, the NASA API only works with dates up to 7 days apart! 
- Assuming that the dates fall in the same month/year
Inputs:
	start_date -> the value associated with the beginning of the search
	end_date   -> the value associated with the end of the search
"""
def month_closest_approaches(start_date, end_date):
	# split the input strings into the corresponding year, month, and day values
	start_year, end_year = int(start_date[0:4]), int(end_date[0:4])
	start_month, end_month = int(start_date[5:7]), int(end_date[5:7])
	start_day, end_day = int(start_date[8:10]), int(end_date[8:10])

	# call the API iff the values between the dates are up to 7 days apart
	if start_year == end_year and start_month == end_month and abs(end_day - start_day) <= 7:
		file = open('src/outputs/month_closest_approaches_OUTPUT.txt', 'a')
		# the link associated with this function is different:
		date_link = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start_date + '&end_date=' + end_date + '&api_key=' + NASA_API_KEY 
		# using the requests library, call the NASA API 
		response = requests.get(date_link)
		# check to make sure the response was valid 
		STATUS_CODE = response.status_code
		if STATUS_CODE == 200:
			response = response.json()
			# print and write to the output file, the output of the response
			print(json.dumps(response, indent=2))
			print('\nFrom ' + start_date + ' to ' + end_date + ' there were ' + str(response['element_count']) + ' asteroid approaches.')
			file.write('\nFrom ' + start_date + ' to ' + end_date + ' there were ' + str(response['element_count']) + ' asteroid approaches.\n\n')
			file.write(json.dumps(response, indent=2))
			file.close()
		# o/w throw exception
		else:
			raise RequestException('Error requesting data from ' + date_link + 'in month_closest_approaches() function...')

	# if the distance between dates is > 7, then recursively call the function with each iterative week
	elif start_year == end_year and start_month == end_month and abs(end_day - start_day) > 7:
		# initialize a counter to see how many weeks are needed to call the API (i.e. (end_day - start_day)/7)
		counter = end_day - start_day
		# initialize a temp_date variable to be the current date in the loop
		temp_date = start_date
		# while the distance (in days) between the end and start days is greater than 0 then recursively compute the asteroid search
		while counter > 0:
			# case when the value between the dates is greater than 7
			if counter > 7:
				month_closest_approaches(temp_date, date_helper(temp_date, 7))
				# update the temporary variables
				temp_date = date_helper(temp_date, 7)
				counter -= 7
			else:
				month_closest_approaches(temp_date, end_date)
				# we are done with the loop
				break

	# o/w the date is not in the propper format
	else:
		raise DateException("Input dates were not in the same year/month, terminating...")

"""
Helper function for the month_closest_approaches() function that returns a new date (in string form) x days ahead of an input date.
Inputs:
	input_date -> initial date to start the calculation
	x          -> number of days after the input_date
"""
def date_helper(input_date, x):
	# split date from year-month-day format
	year = input_date[0:4]
	month = input_date[5:7]
	day = int(input_date[8:10]) + x
	# now check specific cases and update the day value accordingly
	if day < 10:
		day_returned = '0' + str(day)
	elif day > 31:
		raise DateException("Error in date_helper() function. Date goes in between multiple months/years.")
	else:
		day_returned = str(day)
	# return the new string date
	return year + '-' + month + '-' + day_returned


"""
Function that returns the 10 nearest misses (historical or expected) of asteroids impacting Earth
- An astronomical unit (au) is approximatly 150 million kilometers
	- Will determine miss distances based on this value
Input:
	x -> the number of "nearest misses" the user wishes to display
"""
def nearest_misses(x):
	# using the requests library, call the NASA API 
	response = requests.get(link)
	# check to make sure the response was valid 
	STATUS_CODE = response.status_code
	# if successful continue
	if STATUS_CODE == 200:
		# initialize 3 lists used for determining the astronomical unit values, and convert response to json
		au_values = []
		first_iteration_value = []
		second_iteration_value = []
		response = response.json()

		# now loop through the range of the two main lists (in the response json) and append Earth-orbiting asteroid values
		for i in range(len(response['near_earth_objects'])):
			for j in range(len(response['near_earth_objects'][i]['close_approach_data'])):
				# if the current orbital data has an orbiting body of Earth, update the corresponding lists
				if response['near_earth_objects'][i]['close_approach_data'][j]['orbiting_body'] == "Earth":
					au_values.append(response['near_earth_objects'][i]['close_approach_data'][j]['miss_distance']['astronomical'])
					first_iteration_value.append(i)
					second_iteration_value.append(j)

		file = open('src/outputs/nearest_misses_OUTPUT.txt', 'w')
		# now we have 3 lists of corresponding values, so print the minimums by iterating and removing the current min value
		for i in range(x):
			# the temporary index used to determine where in the dictionary the asteroid is
			temp_index = au_values.index(min(au_values))
			# print and write to the output file, the output of the response
			print("Nearest miss number: " + str(i+1))
			print(json.dumps(response['near_earth_objects'][first_iteration_value[temp_index]]['close_approach_data'][second_iteration_value[temp_index]], indent=2))
			file.write("{}\n{}\n".format("Nearest miss number: " + str(i+1), json.dumps(response['near_earth_objects'][first_iteration_value[temp_index]]['close_approach_data'][second_iteration_value[temp_index]], indent=2)))
			# remove the current min index from the lists for the next iteration
			au_values.pop(temp_index)
			first_iteration_value.pop(temp_index)
			second_iteration_value.pop(temp_index)
		file.close()
	# o/w throw exception
	else:
		raise RequestException('Error requesting data from ' + link + 'in nearest_misses() function...')

# "main" method, where the program begins (TESTING WITH USER INPUT)
if __name__ == '__main__':
	print("{}\n{}\n{}\n\n".format("Henry Gardner, hgardne4@u.rochester.edu", "Mashey Asteroid Hunter Technical Interview", "October 15, 2021"))
	print("This project creates a data pipeline to track asteroids based on certain criteria.")
	print("Refer to the outputs folder which contains the output from these functions.")
	print("{}\n\t{}\n\t{}\n\t{}".format("Functions to test", "1. asteroid_closest_approach()", "2. month_closest_approaches()", "3. nearest_misses()"))
	user_input = input("Enter a number to test a corresponding function (i.e. '1' for testing asteroid_closest_approach()): ")
	
	# depending on the user input, complete the corresponding function
# asteroid_closest_approach():
	if int(user_input) == 1:
		print("Testing the asteroid_closest_approach() function: \n")
		asteroid_closest_approach()
		print("Completed the asteroid_closest_approach() function, scroll to top for full output.")
# month_closest_approaches():
	elif int(user_input) == 2:
		# since the month_closest_approaches_OUTPUT.txt file is appended in other functions, need to initialize it as empty
		# instead of deleting the file each time
		file = open('src/outputs/month_closest_approaches_OUTPUT.txt', 'w')
		file.write("")
		file.close()
		print("Testing the month_closest_approaches() function.")
		print("Note that the input dates have to be in the same month.")
		try:
			start_date = input("Enter a start date (year-month-day): ")
			end_date = input("Enter an end_date (year-month-day): ")
			month_closest_approaches(start_date, end_date)
			print("Completed the month_closest_approaches() function, scroll to top for full output.")
		except: 
			raise UserInputException("Unrecognized input, terminating...")
# nearest_misses():
	elif int(user_input) == 3:
		print("Testing the nearest_misses() function:")
		try:
			num_of_nearest_misses = input("Enter the number of nearest misses wished to be displayed: ")
			nearest_misses(int(num_of_nearest_misses))
			print("Completed the nearest_misses() function, scroll to top for full output.")
		except:
			raise UserInputException("Unrecognized input, terminating...")
	else:
		raise UserInputException("Unrecognized input, must enter one of the following numbers {1,2,3}, terminating...")