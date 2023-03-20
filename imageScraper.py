import os
import requests
from bs4 import BeautifulSoup

from utils import mkDirAtCwdIfNoExist

# Replace this URL with the website you want to scrape
url = 'https://www.alibaba.com/pla/Top-Quality-8-1-2x3-outer_1600166530400.html?mark=google_shopping&biz=pla&searchText=other%20wheels+tires+%20accessories&product_id=1600166530400&pcy=US'

# Replace 'class_name' with the class name of the HTML element that contains the images
class_name = 'product-img-nav-item'

# Send a request to the website and get the HTML response
response = requests.get(url)

# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all HTML elements with the specified class name
elements = soup.find_all(class_=class_name)

folderPath = mkDirAtCwdIfNoExist("scraped_images")

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
        filename = (folderPath + "/" + os.path.basename(image_url))
        with open(filename, 'wb') as f:
            f.write(response.content)
