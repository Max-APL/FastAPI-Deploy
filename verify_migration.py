import time
import subprocess
import sys
import os
import requests
import cv2
import numpy as np

def create_dummy_image(filename="test_input.png"):
    # Create a simple 100x100 random image
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    cv2.imwrite(filename, img)
    print(f"Created dummy image: {filename}")

def verify_api():
    # Start the API
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("Started API server on port 8001...")
    
    try:
        # Wait for server to start
        time.sleep(5)
        
        base_url = "http://127.0.0.1:8001"
        
        # 1. Test Root Endpoint
        print("Testing root endpoint...")
        resp = requests.get(f"{base_url}/")
        assert resp.status_code == 200
        assert "Marketing Media Enhancement API" in resp.json()["message"]
        print("Root endpoint verified.")
        
        # 2. Test Enhancement with Platform (Instagram Story)
        print("Testing /enhance-media with platform='instagram_story'...")
        with open("test_input.png", "rb") as f:
            files = {"file": ("test_input.png", f, "image/png")}
            params = {"platform": "instagram_story", "campaign_id": "test_campaign"}
            resp = requests.post(f"{base_url}/enhance-media", files=files, params=params)
        
        assert resp.status_code == 200
        
        # Save output
        with open("output_ig.png", "wb") as f:
            f.write(resp.content)
            
        # Verify dimensions
        img = cv2.imread("output_ig.png")
        h, w = img.shape[:2]
        print(f"Output dimensions: {w}x{h}")
        assert w == 1080
        assert h == 1920
        print("Instagram Story dimensions verified.")

        # 3. Test Enhancement with Platform (Twitter Post)
        print("Testing /enhance-media with platform='twitter_post'...")
        with open("test_input.png", "rb") as f:
            files = {"file": ("test_input.png", f, "image/png")}
            params = {"platform": "twitter_post"}
            resp = requests.post(f"{base_url}/enhance-media", files=files, params=params)
            
        assert resp.status_code == 200
        
        with open("output_twitter.png", "wb") as f:
            f.write(resp.content)
            
        img = cv2.imread("output_twitter.png")
        h, w = img.shape[:2]
        print(f"Output dimensions: {w}x{h}")
        assert w == 1200
        assert h == 675
        print("Twitter Post dimensions verified.")

        print("\nAll tests passed successfully!")

    except Exception as e:
        print(f"Verification failed: {e}")
        # Print server output if failed
        outs, errs = proc.communicate(timeout=1)
        print("Server Output:", outs.decode())
        print("Server Error:", errs.decode())
        raise e
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    create_dummy_image()
    # Install requests if not present? Assumed present or using standard lib would be safer but requests is cleaner.
    # If requests fails we catch it.
    verify_api()
