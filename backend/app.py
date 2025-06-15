from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
from PIL import Image
import numpy as np
import tensorflow as tf

app = FastAPI()

# CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model (once)
model = tf.keras.models.load_model("model.keras")

# Input model size — update this if different
IMG_SIZE = (28, 28)

# Pydantic schema
class ImageData(BaseModel):
    image: str  # base64 string

@app.post("/predict")
async def predict(data: ImageData):
    try:
        # Decode base64 image
        header, encoded = data.image.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(img_bytes)).convert("L")  # grayscale

        # Resize and normalize
        img = img.resize(IMG_SIZE)
        arr = np.array(img).astype("float32") / 255.0
        arr = arr.reshape(1, IMG_SIZE[0], IMG_SIZE[1], 1)  # shape: (1, 28, 28, 1)

        # Predict
        predictions = model.predict(arr)
        predicted_digit = int(np.argmax(predictions))

        return {"prediction": predicted_digit}

    except Exception as e:
        return {"error": str(e)}
