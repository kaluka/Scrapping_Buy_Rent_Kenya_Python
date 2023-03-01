from bs4 import BeautifulSoup
import requests
import re # import regular expression module
import csv # import csv module

base_URL="https://www.buyrentkenya.com/houses-for-rent"

#input your headers here

headers = { }

# create a csv file and write the header row
with open("houses_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Location", "Bedrooms", "Rent"])

# loop through different page numbers
page = 2 # start from page 2
while True:
    # append the page number to the base URL
    
    URL = base_URL + "?page=" + str(page)
    # get and parse the page
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

# get a list of div elements that have the class that contsins the listings
    items = soup.find_all("div", class_="flex flex-col justify-between md:w-2/3 px-5 py-4")

      # if there are no items on the page, break out of the loop
    if not items:
        break
        
    
    for item in items:

        ## get the listing title information
        
        title = item.find("span", class_ ="hidden md:inline").get_text()

        # get the bedrooms information using try and except
        try:
            bedrooms = item.find("span", class_="font-semibold leading-6").get_text()
        except AttributeError: # catch the AttributeError if there is no such element
            bedrooms = "" # assign a default value to bedrooms

        #get lication information
        
        location = item.find("p", class_="text-sm font-normal text-grey-500 truncate ml-1").get_text()      
        
        # get the rent information 
        
        rent = item.find("p", class_="font-bold text-xl leading-7 text-grey-900").get_text() 

        # use regular expression to extract numbers from rent string
        try:
            rent_number = ''.join(re.findall('\d+', rent)) # join the list elements into a single string
            rent_number = int(rent_number) # convert the string into an integer
        except:
            rent_number = 0 # assign 0 if there is no rent information     
        

        # write each row of data into the csv file
        with open("houses_data.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([title, location, bedrooms, rent_number])

     # increment the page number by 1    
    page += 1        

    
