import requests
import random
import os
from PIL import Image
from io import BytesIO
import string
import schedule
import time

# Define your Imgflip API credentials
USERNAME = 'epubbysudsou'
PASSWORD = 'gubluDas2009'

# Folder to save memes
MEME_FOLDER = 'memes'
HTML_FILE = 'index.html'

# Create meme folder if it doesn't exist
if not os.path.exists(MEME_FOLDER):
    os.makedirs(MEME_FOLDER)

# Function to get meme templates
def get_meme_templates():
    response = requests.get('https://api.imgflip.com/get_memes')
    if response.status_code == 200:
        data = response.json()
        return data['data']['memes']
    else:
        print("Error fetching meme templates.")
        return []

# Function to create a meme
def create_meme(template_id, text0, text1):
    url = 'https://api.imgflip.com/caption_image'
    params = {
        'template_id': template_id,
        'username': USERNAME,
        'password': PASSWORD,
        'text0': text0,
        'text1': text1
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            return data['data']['url']
        else:
            print("Error creating meme:", data['error_message'])
            return None
    else:
        print("Error creating meme.")
        return None

# Function to download meme
def download_meme(meme_url, filename):
    response = requests.get(meme_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(os.path.join(MEME_FOLDER, filename))
        print(f"Meme saved as {filename}")
    else:
        print("Error downloading meme.")

# Function to get a random joke
def get_random_joke():
    response = requests.get('https://v2.jokeapi.dev/joke/Any?type=twopart')
    if response.status_code == 200:
        data = response.json()
        return data['setup'], data['delivery']
    else:
        print("Error fetching joke.")
        return None, None

# Function to generate a random filename
def generate_random_filename(extension='jpg'):
    chars = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(chars) for _ in range(10))
    return f"{random_string}.{extension}"

# Function to update HTML file with new meme
def update_html_file(filename):
    with open(HTML_FILE, 'a') as f:
        f.write(f'''
        <div class="meme">
            <img src="{MEME_FOLDER}/{filename}" alt="Meme">
            <div class="actions">
                <button onclick="likeMeme()">Like</button>
                <button onclick="dislikeMeme()">Dislike</button>
            </div>
        </div>
        ''')

# Function to create the initial HTML structure if it doesn't exist
def create_html_structure():
    if not os.path.exists(HTML_FILE):
        with open(HTML_FILE, 'w') as f:
            f.write('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Meme Gallery</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .meme { margin: 20px; border: 1px solid #ccc; padding: 10px; }
                    .actions { margin-top: 10px; }
                    button { margin-right: 10px; }
                </style>
            </head>
            <body>
                <h1>Meme Gallery</h1>
            ''')

# Function to close the HTML structure
def close_html_structure():
    with open(HTML_FILE, 'a') as f:
        f.write('''
            </body>
            </html>
        ''')

# Main function for meme generation and update
def main():
    # Get meme templates
    templates = get_meme_templates()
    if not templates:
        return

    # Select a random template
    template = random.choice(templates)
    template_id = template['id']

    # Get a random joke
    setup, delivery = get_random_joke()
    if setup is None or delivery is None:
        return

    # Create meme
    meme_url = create_meme(template_id, setup, delivery)
    if meme_url:
        # Generate a random filename
        filename = generate_random_filename()

        # Download and save the meme
        download_meme(meme_url, filename)

        # Update HTML file with the new meme
        update_html_file(filename)

# Create the initial HTML structure
create_html_structure()

# Schedule meme generation and update every 5 minutes
schedule.every(1).seconds.do(main)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
