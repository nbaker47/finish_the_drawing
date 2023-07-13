import pytz
import random
from datetime import  datetime
from PIL import Image
from io import BytesIO
import base64
from google.cloud import storage

# Specify the time zone
timezone = pytz.timezone('America/New_York')

# obtain word of the day and daily seed
def get_daily_word_and_seed():
    
    # Get the current time
    current_time = datetime.now(timezone)

    # Print the current time
    print("Current time:", current_time, 'timezone:', timezone)

    # get current date to generate a dailt seed
    current_date = current_time.date()
    
    # set seed for today
    seed = current_date.year * 10000 + current_date.month * 100 + current_date.day
    random.seed(seed)
    
    with open('words.txt', 'r') as file:
        word_list = file.read().split(',')
        
    random_word = random.choice(word_list)
    random_word = random_word.replace(" ", "").title()
    
    print("Random Noun of the Day:", random_word) 
    
    return random_word, seed

# image uploader
def upload_image_to_bucket(drawing_data, username=None):
    
    # Get the image data from the POST request
    base64_image = drawing_data

    # Extract the encoded image data from the base64 string
    encoded_image = base64_image.split(',')[1]

    # Decode the base64 image data
    decoded_image = base64.b64decode(encoded_image)

    # Create a BytesIO object to work with the binary image data
    image_io = BytesIO(decoded_image)

    # Open the image from the BytesIO object
    image = Image.open(image_io)

    # Save the image as PNG to the BytesIO object
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)

    # Set up GCS client
    storage_client = storage.Client()

    # Retrieve the bucket
    bucket = storage_client.bucket('drawoff-391919.appspot.com')

    # Generate a unique filename
    if username is not None:
        filename = f"profilepic_{username}.png"
    else:
        filename = f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

    # Upload the image data to the bucket
    blob = bucket.blob(filename)
    blob.upload_from_file(image_io, content_type='image/png')
    image_url = blob.public_url
    
    return image_url, filename