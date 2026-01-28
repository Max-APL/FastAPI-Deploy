import time
import subprocess
import sys
import os
import urllib.request
import urllib.parse
import json
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
        with urllib.request.urlopen(f"{base_url}/") as response:
            assert response.status == 200
            data = json.loads(response.read().decode())
            assert "Marketing Media Enhancement API" in data["message"]
            print("Root endpoint verified.")
        
        # Function to post multipart form data
        def post_image(url, filepath, params=None):
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            data = []
            
            # Add file
            with open(filepath, 'rb') as f:
                file_content = f.read()
                
            data.append(f'--{boundary}'.encode())
            data.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(filepath)}"'.encode())
            data.append('Content-Type: image/png'.encode())
            data.append(b'')
            data.append(file_content)
            
            data.append(f'--{boundary}--'.encode())
            data.append(b'')
            
            body = b'\r\n'.join(data)
            
            full_url = url
            if params:
                query_string = urllib.parse.urlencode(params)
                full_url = f"{url}?{query_string}"
                
            req = urllib.request.Request(full_url, data=body, method='POST')
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            
            with urllib.request.urlopen(req) as response:
                return response.read()

        # 2. Test Enhancement with Platform (Instagram Story)
        print("Testing /enhance-media with platform='instagram_story'...")
        params = {"platform": "instagram_story", "campaign_id": "test_campaign"}
        content = post_image(f"{base_url}/enhance-media", "test_input.png", params)
        
        # Save output
        with open("output_ig.png", "wb") as f:
            f.write(content)
            
        # Verify dimensions
        img = cv2.imread("output_ig.png")
        if img is None:
             raise Exception("Failed to read output_ig.png")
        h, w = img.shape[:2]
        print(f"Output dimensions: {w}x{h}")
        assert w == 1080
        assert h == 1920
        print("Instagram Story dimensions verified.")

        # 3. Test Enhancement with Platform (Twitter Post)
        print("Testing /enhance-media with platform='twitter_post'...")
        params = {"platform": "twitter_post"}
        content = post_image(f"{base_url}/enhance-media", "test_input.png", params)
            
        with open("output_twitter.png", "wb") as f:
            f.write(content)
            
        img = cv2.imread("output_twitter.png")
        if img is None:
             raise Exception("Failed to read output_twitter.png")
        h, w = img.shape[:2]
        print(f"Output dimensions: {w}x{h}")
        assert w == 1200
        assert h == 675
        print("Twitter Post dimensions verified.")

        print("\nAll tests passed successfully!")

    except Exception as e:
        print(f"Verification failed: {e}")
        # Print server output if failed (non-blocking read would be better but simple here)
        # We can't easily get stdout/stderr here without blocking if verify_api fails early
        # but killing process will release file handles.
        raise e
    finally:
        proc.terminate()
        proc.wait()
        # Print logs
        outs, errs = proc.communicate(timeout=1)
        if outs: print("Server Output:", outs.decode())
        if errs: print("Server Error:", errs.decode())

if __name__ == "__main__":
    create_dummy_image()
    verify_api()
