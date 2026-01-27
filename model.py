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
        # Try to use GPU (OpenCL) if available, otherwise CPU
        self.sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
        self.sr.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """
        Decodes the image to a NumPy array (OpenCV format).
        Checks for max dimension to prevent timeouts.
        """
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Check size (Limit to 1024px to prevent infinite loading on CPU)
        height, width = image.shape[:2]
        max_dim = 1024
        if max(height, width) > max_dim:
            # Calculate new size maintaining aspect ratio
            scaling_factor = max_dim / float(max(height, width))
            new_size = (int(width * scaling_factor), int(height * scaling_factor))
            image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
            print(f"Image resized to {new_size} for performance.")
            
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

    def _crop_center(self, image: np.ndarray, target_w: int, target_h: int) -> np.ndarray:
        h, w = image.shape[:2]
        start_x = max(0, w // 2 - target_w // 2)
        start_y = max(0, h // 2 - target_h // 2)
        return image[start_y:start_y+target_h, start_x:start_x+target_w]

    def resize_for_platform(self, image: np.ndarray, platform: str) -> np.ndarray:
        """
        Resizes and crops the image to fit specific social media platform requirements.
        """
        specs = {
            "instagram_story": (1080, 1920),
            "linkedin_post": (1200, 627),
            "twitter_post": (1200, 675)
        }
        
        if platform not in specs:
            return image
            
        target_w, target_h = specs[platform]
        
        # Calculate scaling to cover the target area (Cover strategy)
        h, w = image.shape[:2]
        scale = max(target_w / w, target_h / h)
        
        # Resize with high quality interpolation
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Crop center to exact dimensions
        return self._crop_center(resized, target_w, target_h)

    def postprocess(self, image: np.ndarray) -> bytes:
        """
        Converts the OpenCV image (numpy array) back to bytes.
        """
        # Encode image to PNG
        _, img_encoded = cv2.imencode('.png', image)
        return img_encoded.tobytes()

# Singleton instance
sr_model = SuperResolutionModel()
