The csv_reader reads each row separately and stores it.We then move through ach row one by one through the for loop, fetching the url at each instant. We then check the URL and throw an error message if it shows a 404 error message. Else if the the response message is 200 we call a function scrap_data() which has a driver function which
automates the web browser interaction. We scraped the data using ID and Xpath and stored the data in an array and also in databese. At the end of the program we are inserting the data in a json file.
