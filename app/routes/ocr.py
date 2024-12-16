from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import pytesseract
from app.utils.nlp import extract_events_from_text
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes

router = APIRouter()

@router.post("/ocr")
async def perform_ocr(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()

    if file.filename.lower().endswith(".pdf"):
        images = convert_from_bytes(contents)
        if not images:
            raise HTTPException(status_code=400, detail="No pages found in PDF")
        extracted_text = pytesseract.image_to_string(images[0])
    else:
        image = Image.open(BytesIO(contents))
        extracted_text = pytesseract.image_to_string(image)

    events_data = extract_events_from_text(extracted_text)
    return {"extracted_events": events_data}
