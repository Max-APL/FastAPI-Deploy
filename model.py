# import tensorflow as tf
# import numpy as np
from PIL import Image
import io

class SuperResolutionModel:
    def __init__(self):
        # TensorFlow is not compatible with Python 3.14 yet.
        # We are using Pillow for the resizing logic as a fallback to ensure the API works.
        pass

    def preprocess(self, image_bytes: bytes) -> Image.Image:
        """
        Decodes the image.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return image

    def predict(self, image: Image.Image) -> Image.Image:
        """
        Upscales the image using bicubic interpolation.
        """
        original_width, original_height = image.size
        
        target_width = original_width * 2
        target_height = original_height * 2
        
        # Using Pillow's resize operation
        upscaled = image.resize(
            (target_width, target_height),
            resample=Image.BICUBIC
        )
        
        return upscaled

    def postprocess(self, image: Image.Image) -> bytes:
        """
        Converts the image back to bytes.
        """
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

# Singleton instance
sr_model = SuperResolutionModel()
