from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import io
from model import sr_model

app = FastAPI(
    title="TensorFlow Image Super-Resolution API",
    description="API to upscale images using TensorFlow",
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
    return {"message": "Welcome to the Image Super-Resolution API. Use POST /upscale to enhance images."}

@app.post("/upscale")
async def upscale_image(file: UploadFile = File(...)):
    """
    Upload an image file to receive an upscaled version.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image using an appropriate Content-Type.")

    try:
        contents = await file.read()
        
        # 1. Preprocess
        input_tensor = sr_model.preprocess(contents)
        
        # 2. Inference
        output_tensor = sr_model.predict(input_tensor)
        
        # 3. Postprocess
        output_bytes = sr_model.postprocess(output_tensor)
        
        return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
