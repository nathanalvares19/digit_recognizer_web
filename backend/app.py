from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
from PIL import Image
import numpy as np
import tensorflow as tf

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "BACKEND IS LIVE!"}

# Load model once at startup
model = tf.keras.models.load_model("./digit_model.keras")

# Standard size for input
IMG_SIZE = (28, 28)

class ImageData(BaseModel):
    image: str  # base64-encoded PNG

@app.post("/predict")
async def predict(data: ImageData):
    try:
        # Decode image
        header, encoded = data.image.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(img_bytes)).convert("L")  # grayscale

        # Preprocess: resize, invert, normalize
        img = img.resize(IMG_SIZE)
        arr = np.array(img).astype("float32")
        arr = 255.0 - arr  # invert to match training
        arr /= 255.0       # normalize to [0, 1]
        arr = arr.reshape(1, 28, 28)  # match model input

        # Predict
        predictions = model.predict(arr)
        predicted_digit = int(np.argmax(predictions))

        return {"prediction": predicted_digit}

    except Exception as e:
        return {"error": str(e)}
