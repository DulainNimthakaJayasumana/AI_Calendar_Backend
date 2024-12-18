from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract
from app.utils.nlp import extract_events_from_text
from app.routes.auth import insert_event_into_google_calendar

router = APIRouter()

@router.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.lower().endswith(".pdf"):
        images = convert_from_bytes(contents)
        if not images:
            raise HTTPException(status_code=400, detail="No pages found in PDF")
        image = images[0]
    else:
        image = Image.open(BytesIO(contents))

    # Perform OCR
    extracted_text = pytesseract.image_to_string(image)
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text detected in the image")

    # Debug log for extracted text
    print(f"Extracted OCR Text:\n{extracted_text}")

    # Extract events using NLP
    events_data = extract_events_from_text(extracted_text)
    if not events_data:
        raise HTTPException(status_code=400, detail="No events detected in the text")

    # Add events to Google Calendar
    added_events = []
    for event in events_data:
        created_event = insert_event_into_google_calendar(event)
        added_events.append(created_event)

    return {"message": "Events added to Google Calendar", "events": added_events}
