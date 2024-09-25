from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import openai
import io
import os
from PIL import Image

app = FastAPI()

# Replace with your actual OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def convert_image_to_text(image_bytes: bytes) -> str:
    """
    Converts image bytes to text using OpenAI's GPT-4 API.

    Args:
        image_bytes (bytes): The image data in bytes.

    Returns:
        str: The text extracted from the image.
    """
    try:
        response = openai.Image.create(
            file=io.BytesIO(image_bytes), purpose="image_to_text", model="gpt-4"
        )
        text = response.get("text", "")
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert_image")
async def convert_image(file: UploadFile = File(...)):
    """
    Endpoint to convert an uploaded image to text using GPT-4.

    Args:
        file (UploadFile): The image file uploaded by the user.

    Returns:
        JSONResponse: A JSON object containing the extracted text.
    """
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid image type. Only PNG and JPEG are supported.",
        )

    try:
        image_bytes = await file.read()
        text = convert_image_to_text(image_bytes)
        return JSONResponse(content={"extracted_text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
