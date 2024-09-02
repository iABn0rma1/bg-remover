from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rembg import remove
from io import BytesIO
from PIL import Image
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=StreamingResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    try:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Please upload a JPEG or PNG image.")

        input_image = Image.open(BytesIO(await file.read()))
        output_image = remove(input_image)

        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        logger.info(f"Successfully processed image: {file.filename}")

        return StreamingResponse(output_buffer, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to process the image. Please try again."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="info")