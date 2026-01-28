from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import io
from model import image_enhancer

app = FastAPI(
    title="Marketing Media Enhancement API",
    description="API to enhance and optimize images for marketing campaigns.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the Marketing Media Enhancement API. Use POST /enhance-media to optimize images."}

@app.post("/enhance-media")
async def enhance_media(
    campaign_id: Optional[str] = None,
    platform: Optional[str] = None,
    file: UploadFile = File(...)
):
    """
    Upload an image file to receive an enhanced and platform-optimized version.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image using an appropriate Content-Type.")

    try:
        if campaign_id:
            print(f"Processing image for campaign: {campaign_id}")

        contents = await file.read()
        
        # 1. Preprocess
        input_image = image_enhancer.preprocess(contents)
        
        # 2. Platform Optimization (Directly on preprocessed image, skipping AI upscale)
        optimized_image = image_enhancer.resize_for_platform(input_image, platform)
        
        # 3. Postprocess
        output_bytes = image_enhancer.postprocess(optimized_image)
        
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
