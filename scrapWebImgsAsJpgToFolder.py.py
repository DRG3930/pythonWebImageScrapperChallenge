import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, folder):
    counter = 1
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    for img in img_tags:
        # Get the source URL of the image
        img_url = img.get('src')
        # Construct the full URL (in case the src is relative)
        full_img_url = urljoin(url, img_url).split('?')[0]
        print('img url: ',full_img_url)

        try:
            # Get the image content
            img_response = requests.get(full_img_url)
            img_response.raise_for_status()  # Raise an error for bad status

            # Get the image file name
            img_name = os.path.basename(full_img_url)

            # Save the image as a JPEG file
            img_path = os.path.join(folder, img_name) + str(counter) + ".jpg"
            counter += 1
            print('saving file: ', img_path)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_response.content)
                print(f"Downloaded {img_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {full_img_url}: {e}")


if __name__ == "__main__":
    page_url = 'https://www.troostwijkauctions.com/en?msockid=34dde33d135f69e03dcef6bb12e568bf'
    download_folder = 'C:/Users/Chris/downloadedImgsToShowWorking'
    download_images(page_url, download_folder)
