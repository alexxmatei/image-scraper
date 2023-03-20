import os
import requests
from bs4 import BeautifulSoup

# Replace this URL with the website you want to scrape
url = ''

# Replace 'class_name' with the class name of the HTML element that contains the images
class_name = ''

# Send a request to the website and get the HTML response
response = requests.get(url)

# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all HTML elements with the specified class name
elements = soup.find_all(class_=class_name)

# Loop through all elements and find the image URLs
for element in elements:
    image_urls = [img['src'] for img in element.find_all('img')]

    # Loop through all image URLs and download the images
    for image_url in image_urls:
        # If the url doesn't start with https:, but with //, add the https:
        if image_url.startswith('//'):
            image_url = f'https:{image_url}'
        print(image_url)
        response = requests.get(image_url)
        filename = os.path.join(
            os.getcwd(), "scraped_images", os.path.basename(image_url))
        print(filename)
        with open(filename, 'wb') as f:
            f.write(response.content)
