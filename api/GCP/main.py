# Imports
from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np


# Constants

# Bucket is like google drive. Our model is uploaded in that bucket
BUCKET_NAME = "bucket-for-tools-and-tech-project"
# Our model file path
SOURCE_BLOB_NAME = "models/1.h5"
# Location where we'll download model file
DISTINATION_FILE_NAME = "/tmp/potateos.h5"

# Class names for our problem
CLASS_NAMES = ["Early blight", "Late blight", "Healthy"]


model = None


# This is the function which provides api for our webapp
def predict(request):
    # Handling preflight requests
    # This is required due to CORS restrictions in browsers
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "https://potato-disease.netlify.app/",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Handling main requests
    header = {"Access-Control-Allow-Origin": "*"}

    # Bad requests
    if request.method != "POST":
        return ("Bad request", 400, header)

    # Handling 
    global model
    if model is None:
        # Loading model if its none
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(SOURCE_BLOB_NAME)
        blob.download_to_filename(DISTINATION_FILE_NAME)
        model = tf.keras.models.load_model(DISTINATION_FILE_NAME)

    # Some preprocessing
    image = request.files["file"]       # Loading image from client request
    img = np.array(
        Image.open(image)\
            .convert("RGB")\
            .resize((256, 256))
    )                                   # Loading image & resizing it
    imgs = tf.expand_dims(img, 0)       # Creating an array of images (This is required because our model expects multiple images)

    predictions = model.predict(imgs)   # Making prediction
    print(predictions)

    # Getting class label and confidence for max confident class
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    dict_to_return = {
        "classLabel": predicted_class,
        "confidence": float(confidence),
    }

    return (dict_to_return, 200, header)
