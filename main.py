import requests
from bs4 import BeautifulSoup
import time  # Added for delays
import logging  # Added for logging
from tqdm import tqdm  # Added for progress bar

def scrape_unsplash_images(search_query, num_images):
    # Set up logging
    import os

    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'unsplash_scraper.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Base URL for Unsplash search
    base_url = f"https://unsplash.com/s/photos/{search_query}"

    # Create directory to save images

    # Get the path to the user's Downloads directory
    downloads_dir = os.path.expanduser('~/Downloads')

    # Create directory to save images
    save_dir = os.path.join(downloads_dir, f"{search_query}_images")
    os.makedirs(save_dir, exist_ok=True)

    # Extract image URLs with error handling
    image_urls = []
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        for img in soup.find_all('img'):
            if img.has_attr('src') and img['src'].startswith('https://images.unsplash.com/photo'):
                image_urls.append(img['src'])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching images: {e}")
        return

    # Download images with progress bar and error handling
    for i, url in tqdm(enumerate(image_urls[:num_images], 1), desc="Downloading images"):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Extract image format from response headers
            image_format = response.headers.get('Content-Type').split('/')[1]
            image_name = f"{search_query}_{i}.{image_format}"
            image_path = os.path.join(save_dir, image_name)

            with open(image_path, 'wb') as f:
                f.write(response.content)

            logging.info(f"Downloaded image {i}/{num_images}: {image_name}")

            # Delay to avoid rate limiting
            time.sleep(0.5)  # Adjust delay as needed

        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading image {i}: {e}")

# Get user input for search query and number of images
search_query = input("Enter search query: ")
num_images = int(input("Enter number of images to download: "))

scrape_unsplash_images(search_query, num_images)
