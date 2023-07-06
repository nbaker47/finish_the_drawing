# Imports the Google Cloud client library
from google.cloud import storage
import os

# Set the environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\bunny\AppData\Roaming\gcloud\application_default_credentials.json'

# Instantiates a client
storage_client = storage.Client()

# The name for the new bucket
bucket_name = "submissions"

bucket = storage_client.bucket(bucket_name)
blob = bucket.blob("test.txt")
blob.upload_from_string("image_data", content_type='text/txt')  # Modify the content type based on the image format

print(f"Bucket {bucket.name} created.")