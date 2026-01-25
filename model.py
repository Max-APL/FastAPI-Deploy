import cv2
from cv2 import dnn_superres
import numpy as np
import io

class SuperResolutionModel:
    def __init__(self):
        self.sr = dnn_superres.DnnSuperResImpl_create()
        # Read the model
        path = "EDSR_x4.pb"
        self.sr.readModel(path)
        # Set the model and scale
        self.sr.setModel("edsr", 4)

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """
        Decodes the image to a NumPy array (OpenCV format).
        """
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image

    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Upscales the image using the EDSR model and applies clean sharpening.
        """
        # Upscale
        result = self.sr.upsample(image)
        
        # Apply clean sharpening kernel (Edge Enhancement)
        # This kernel enhances edges without oversaturating colors like CLAHE
        kernel = np.array([[-1,-1,-1], 
                           [-1, 9,-1], 
                           [-1,-1,-1]])
                           
        # Apply the sharpening kernel
        sharpened = cv2.filter2D(result, -1, kernel)
        
        # Mix with original upscaled result to avoid too much noise (Weighted add)
        # 0.7 * Sharpened + 0.3 * Smooth Upscale
        final_result = cv2.addWeighted(sharpened, 0.6, result, 0.4, 0)
        
        return final_result

    def postprocess(self, image: np.ndarray) -> bytes:
        """
        Converts the OpenCV image (numpy array) back to bytes.
        """
        # Encode image to PNG
        _, img_encoded = cv2.imencode('.png', image)
        return img_encoded.tobytes()

# Singleton instance
sr_model = SuperResolutionModel()
