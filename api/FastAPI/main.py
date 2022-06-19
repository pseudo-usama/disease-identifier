# Imports
import numpy as np
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from tensorflow.keras.models import load_model


# Constants
MODEL = load_model('models/1.h5')
CLASS_NAMES = ['Early blight', 'Late blight', 'Healthy']

# Api server
app = FastAPI()

# Handling CORS
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/predict')
async def predict(
    file: UploadFile = File(...)
):
    # Reading image and making prediction
    img = read_file_as_img(await file.read())
    predictions = MODEL.predict(np.expand_dims(img, 0))
    prediction = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    dict_to_return = {
        'classLabel': prediction,
        'confidence': float(confidence)
    }
    print(dict_to_return)

    return dict_to_return


def read_file_as_img(data) -> np.ndarray:
    return np.array(Image.open(BytesIO(data)).resize((256, 256)))


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)
