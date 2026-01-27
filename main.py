from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import io
from model import sr_model

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
        input_tensor = sr_model.preprocess(contents)
        
        # 2. Inference (Upscale)
        upscaled_image = sr_model.predict(input_tensor)

        # 3. Platform Optimization
        optimized_image = sr_model.resize_for_platform(upscaled_image, platform)
        
        # 4. Postprocess
        output_bytes = sr_model.postprocess(optimized_image)
        
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
