import os
from fastapi import UploadFile, File
from typing import List
import PyPDF2
import docx2txt

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

async def validate_and_extract(files: List[UploadFile] = File(...)):
    texts = []
    for file in files:
        if file.size > MAX_FILE_SIZE:
            raise ValueError("File too large")
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise ValueError("Only PDF/DOCX allowed")
        
        content = await file.read()
        if file.filename.lower().endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file.file)
            text = ''.join(page.extract_text() for page in pdf_reader.pages)
        else:
            text = docx2txt.process(file.file)
        texts.append({"filename": file.filename, "text": text})
    return texts

