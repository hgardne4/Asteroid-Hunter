Henry Gardner, hgardne4@u.rochester.edu
Mashey Asteroid Hunter Technical Project Interview
October 15, 2021

I completed this project in Python3.

Folders:
    instructions -> folder containing all the information provided
    src          -> folder containing my solution
    src/outputs  -> folder containing the outputs to the individual functions

Files:
    README.txt                                       -> my project explanation
    Makefile                                         -> file that runs the project
    instructions/README.md                           -> directions for the project provided
    src/asteroid_hunter.py                           -> my Python3 solution
    src/outputs/asteroid_closest_approach_OUTPUT.txt -> output file from testing the asteroid_closest_approach() function
    src/outputs/month_closest_approaches_OUTPUT.txt  -> output file from testing the month_closest_approaches() function
    src/outputs/nearest_misses_OUTPUT.txt            -> output file from testing the nearest_misses() function

How to "run"/"execute" the project:
    Enter into the Asteroid-Hunter folder and then run the following command:

            "make"

    This will automatically call the Makefile that I created and will execute the Python3 code 

Notes:
    User Input:
        This project involves user input to test specific instances of each function. For example, the program will 
        ask to enter a start and end date when performing the month_closest_approaches() function, and asks for a 
        integer to specify how many of the "nearest misses" the user wishes to display in the nearest_misses() 
        function. I have created exception classes that handle specific cases when the input is "faulty," so to speak.

    Exception Handling:
        Although not required, I decided to work on my exception handling by creating the followig exceptions:

            - RequestException   -> raised if the request to the NASA API is not successful
            - DateException      -> raised if an error appears when parsing the string dates 
            - UserInputException -> raised if the user enters an unexpected sequence of characters

        Upon an error, these exceptions will automatically be caught and notify the user.

    Extended Capabilities:
        I added output files to store specific instances of an example code execution. Additionally, I added the ability
        for the user to enter in how many "nearest misses" they wished to display in the nearest_misses() funciton although
        I was only asked to output the first 10. 

    Assumptions:
        With the provided information, I made some assumptions on the output and ways to solve the functions. 
        I made the assumption that the month_closest_approaches() function takes in two dates that appear in the
        same month and year. The NASA API only handles the situations when the input dates are up to 7 days apart,
        but I managed to work around that calling the API with specific iterations of an extended date range. 
        I also assumed that the "nearest misses" could be calculated in the astronomical section in the miss distance
        tag in the json response from the NASA API. Additionally, the nearest misses could be from the same asteroid,
        so to speak.

    asteroid_closest_approach_OUTPUT.txt():
        This was the first problem to solve and was straight forward once I understood the NASA API. After recieving
        a response from the API, I just needed to loop through the range of the near_earth_objects and update the 
        close_approach_data list. After analyzing the json response, I assumed that the astronomical distance value
        would be the easiest to determine as the "closest." Therefore, I just needed to loop through the 
        close_approach_data list and return the index with the smallest astronomical value.

    month_closest_approaches():
        This was the second problem to solve and required a different API link. This problem was trickier than the first
        because the NASA API only allows for the start and end dates to be 7 days apart. I made the assumption that the 
        months and years needed to be the same. Therefore, if the difference between the end date and the start date was 
        less than or equal to 7, I just needed to call the API with the provided endpoint. If this distance was greater than
        7, I made a iterative solution that recursively calls the month_closest_approaches() with temporary dates of max
        distance 7 days apart. To clean up the code, I made a helper function that would return a new date (string format)
        with an input number of days ahead of a previous date.

    nearest_misses():
        This was the third and final problem that needed to be solved. This question wanted to output the 10 nearest misses expected or historical. 
        I added the ability to enter in the number of nearest misses. This solution was similar to the first one, except I needed to keep track of 
        the au_values for 2 sets of iterations. Therefore, I generated two loops and made a list: au_values, that had each au_value in both iterations. 
        I then found the min value of the au_value list, would output the asteroid information, and then remove that index from the au_list lists to find 
        the next min value in the next phase of the iteration. This would be completed x number of times, where x is the integer the user input.
        This is a slow solution, but one that works. If I had some more time to work, I would have conisdered was to optimize such as removing the 
        two instances of doulbe looping through the whole data. The problem is that this question asked for the 10 nearest misses, and 2 or more of these
        nearest misses could have been from the same asteroid, that is why I decided to approach this problem in the way I did. 

Questions/Comments:
    If there are any questions/comments about my solution, feel free to reach out via email: hgardne4@u.rochester.edu