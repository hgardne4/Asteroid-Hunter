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
Function that prints out the json data returned by the NASA API with only the closest approach returned per asteroid.
Need to change the list of close_approach_data to be a single element containing only the minimum distance value.
Assuming this minimum distance value is an astronomical unit:
	- An astronomical unit (au) is approximatly 150 million kilometers
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
			# initialize a list that will have all the current au_values for this particular asteroid
			au_values = []
			# loop through the close_approach_data list for this asteroid and update the au_values list iff it's orbiting body is Earth
			for j in range(len(response[i]['close_approach_data'])):
				if response[i]['close_approach_data'][j]['orbiting_body'] == "Earth":
					au_values.append(float(response[i]['close_approach_data'][j]['miss_distance']['astronomical']))
			# determine the minimum value of this list
			min_val = min(au_values)
			# update the close_approach_data to contain only the min element using a list comprehension
			response[i]['close_approach_data'] = [response[i]['close_approach_data'][x] for x in range(len(response[i]['close_approach_data'])) if (float(response[i]['close_approach_data'][x]['miss_distance']['astronomical']) == min_val)][0]
			# print and write to the output file, the output of the response
			print("ASTEROID NUMER: " + str(i+1) + " with MIN VAL: " + str(min_val))
			file.write('{}\n{}\n\n'.format("ASTEROID NUMER: " + str(i+1) + " with MIN VAL: " + str(min_val), json.dumps(response[i], indent=2)))
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
		# initialize a counter to see how many calls are needed to the API (i.e. ceiling([end_day - start_day]/7))
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
	# assumption that the dates must fall in the same month/year
	elif day > 31:
		raise DateException("Error in date_helper() function. Date goes in between multiple months/years.")
	else:
		day_returned = str(day)
	# return the new string date
	return year + '-' + month + '-' + day_returned


"""
Function that returns the x nearest misses (historical or expected) of asteroids impacting Earth.
- An astronomical unit (au) is approximatly 150 million kilometers
	- Will determine miss distances based on this value
Input:
	x -> the number of "nearest misses" the user wishes to display (the requirments only required to display 10)
"""
def nearest_misses(x):
	# using the requests library, call the NASA API 
	response = requests.get(link)
	# check to make sure the response was valid 
	STATUS_CODE = response.status_code
	# if successful continue
	if STATUS_CODE == 200:
		# initialize a list used for determining the astronomical unit values, and convert response to json
		au_values = []
		response = response.json()

		# now loop through the range of the two main lists (in the response json) and append Earth-orbiting asteroid values
		for i in range(len(response['near_earth_objects'])):
			for j in range(len(response['near_earth_objects'][i]['close_approach_data'])):
				# if the current orbital data has an orbiting body of Earth, update the corresponding lists
				if response['near_earth_objects'][i]['close_approach_data'][j]['orbiting_body'] == "Earth":
					au_values.append(float(response['near_earth_objects'][i]['close_approach_data'][j]['miss_distance']['astronomical']))
		
		file = open('src/outputs/nearest_misses_OUTPUT.txt', 'a')

		# now we have a list of all the au_values, so loop through the input number and print the associated data for that min value
		for i in range(x):
			# boolean value used to save computation time and determines when to break the loop
			found = False
			# the temporary index used to determine where in the dictionary the asteroid is
			current_min = min(au_values)
			# loop through all the values in the lists of near earth object and close approach data 
			for j in range(len(response['near_earth_objects'])):
				for k in range(len(response['near_earth_objects'][j]['close_approach_data'])):
					# check to see if the current au_value is the min, if so print and break current loop
					if float(response['near_earth_objects'][j]['close_approach_data'][k]['miss_distance']['astronomical']) == current_min:
						# need to store the current list of close_approach_data in a temporary variable to re-update after printing
						temp = response['near_earth_objects'][j]['close_approach_data']
						# set the close_approach_data list to only contain the value with the lowest miss_distance
						response['near_earth_objects'][j]['close_approach_data'] = [response['near_earth_objects'][j]['close_approach_data'][k]]
						# print and write to the output file, the output of the response
						print("\nNearest miss number: " + str(i+1) + " with MIN VAL: " + str(current_min))
						print(json.dumps(response['near_earth_objects'][j], indent=2))
						file.write("\n{}\n{}\n".format("Nearest miss number: " + str(i+1) + " with MIN VAL: " + str(current_min), json.dumps(response['near_earth_objects'][j], indent=2)))
						# change the close_approach_data back to the original list
						response['near_earth_objects'][j]['close_approach_data'] = temp
						# break the double loop and continue to the next mon value
						found = True
						break
				if found:
					break
			# remove the current min from the au_list for the next iteration
			au_values.remove(current_min)
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
	# depending on the user input, complete the corresponding function
	user_input = input("Enter a number to test a corresponding function (i.e. '1' for testing asteroid_closest_approach()): ")
	
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
		# since the month_closest_approaches_OUTPUT.txt file is appended in other functions, need to initialize it as empty
		# instead of deleting the file each time
		file = open('src/outputs/nearest_misses_OUTPUT.txt', 'w')
		file.write("")
		file.close()
		print("Testing the nearest_misses() function:")
		try:
			num_of_nearest_misses = input("Enter the number of nearest misses wished to be displayed: ")
			nearest_misses(int(num_of_nearest_misses))
			print("Completed the nearest_misses() function, scroll to top for full output.")
		except:
			raise UserInputException("Unrecognized input, terminating...")
	else:
		raise UserInputException("Unrecognized input, must enter one of the following numbers {1,2,3}, terminating...")