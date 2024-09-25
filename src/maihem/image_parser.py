import pymupdf  # PyMuPDF
from docx import Document
from PIL import Image
import io
import os
import requests


def extract_images_and_convert_text(document_path):
    """
    Extracts images from a PDF or DOCX document and converts them into text using an LLM.

    Args:
        document_path (str): The path to the PDF or DOCX document.

    Returns:
        dict: A dictionary where keys are image file names and values are the extracted text.
    """
    extracted_text = {}
    file_extension = os.path.splitext(document_path)[1].lower()

    if file_extension == ".pdf":
        extracted_text = _process_pdf(document_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

    return extracted_text


def _process_pdf(pdf_path):
    """
    Extracts images from a PDF and converts them into text using an LLM.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary where keys are image identifiers and values are the extracted text.
    """
    extracted = {}
    doc = pymupdf.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))

            # Convert image to bytes for API
            buffered = io.BytesIO()
            image.save(buffered, format=image_ext.upper())
            img_bytes = buffered.getvalue()

            # Query LLM
            text = _query_llm(img_bytes)
            image_id = f"page_{page_num+1}_image_{img_index+1}.{image_ext}"
            extracted[image_id] = text

    return extracted


def _query_llm(image_bytes):
    """
    Sends the image bytes to an LLM API to convert the image into text.

    Args:
        image_bytes (bytes): The image data in bytes.

    Returns:
        str: The text extracted from the image.
    """
    api_url = "https://api.your-llm-service.com/convert-image"
    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN",
        "Content-Type": "application/octet-stream",
    }
    response = requests.post(api_url, headers=headers, data=image_bytes)

    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return ""
