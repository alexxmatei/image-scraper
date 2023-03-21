from utils import mkDirAtCwdIfNoExist
import os
import requests
from bs4 import BeautifulSoup
import csv

# Specify the CSV file path
csv_file_path = 'example.csv'

# Initialize an empty list to hold the data
csv_data = []

# Open the CSV file using a context manager
with open(csv_file_path, 'r') as csv_file:

    # Use the CSV reader to parse the file
    csv_reader = csv.reader(csv_file)

    # Loop through each row in the CSV file
    for row in csv_reader:

        # Append the entire row to the data list
        csv_data.append(row)

# Create a directory to save the downloaded images if it doesn't already exist
mkDirAtCwdIfNoExist("scraped_images")

for row in csv_data:
    # Create a folder for the current row in the scraped_images directory
    folderPath = mkDirAtCwdIfNoExist(f"scraped_images/{row[0]}")
    url = row[1]
    if url != '':
        print(url)

        # Replace 'class_name' with the class name of the HTML element that
        # contains the images
        # TODO - Give the class name as argument when calling script OR
        # TODO - Add it to an envar
        class_name = ''

        # Send a request to the website and get the HTML response
        response = requests.get(url)

        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all HTML elements with the specified class name
        elements = soup.find_all(class_=class_name)

        # Loop through all elements and find the image URLs
        for element in elements:
            # Get a list of all image URLs within the current element
            image_urls = [img['src'] for img in element.find_all('img')]

            # Loop through all image URLs and download the images
            for image_url in image_urls:
                # Get the index of the last occurrence of '.png' or '.jpg'
                png_index = image_url.find(".png")
                jpg_index = image_url.find(".jpg")
                IMAGE_FORMAT_STRING_LENGTH = 4
                index = max(png_index, jpg_index) + IMAGE_FORMAT_STRING_LENGTH

                # Extract the substring until the index to get the image URL
                # We do this to remove the extra image resize queries at the end
                image_url = image_url[:index]
                # If the URL starts with // instead of https://,
                # add the https:// prefix
                if image_url.startswith('//'):
                    image_url = f'https:{image_url}'
                print(image_url)

                # Download the image and save it to the appropriate folder
                response = requests.get(image_url)
                filename = (folderPath + "/" + os.path.basename(image_url))
                with open(filename, 'wb') as f:
                    f.write(response.content)
