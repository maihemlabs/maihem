import os
import pymupdf
import docx2txt


def extract_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return extract_pdf_text(file_path)
    elif file_extension == ".docx":
        return extract_docx_text(file_path)
    elif file_extension in [".txt", ".md"]:
        return extract_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def extract_pdf_text(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_docx_text(file_path):
    text = docx2txt.process(file_path)
    return text


def extract_text_file(file_path):
    doc = pymupdf.open(file_path, filetype="txt")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
