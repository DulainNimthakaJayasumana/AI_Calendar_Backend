import spacy
import dateparser

nlp = spacy.load("en_core_web_sm")

def extract_events_from_text(text: str):
    doc = nlp(text)
    events = []
    event_keywords = ["meeting", "event", "appointment", "schedule", "conference", "seminar"]

    for sent in doc.sents:
        sentence_text = sent.text.strip().lower()
        if any(keyword in sentence_text for keyword in event_keywords):
            event_datetime = dateparser.parse(sentence_text)
            entities = {ent.label_: ent.text for ent in sent.ents}
            if "PERSON" in entities:
                title = f"Meeting with {entities['PERSON']}"
            elif "ORG" in entities:
                title = f"Meeting with {entities['ORG']}"
            else:
                title = sent.text.strip().capitalize()

            if event_datetime:
                end_time = event_datetime
                if event_datetime.hour is not None:
                    end_time = end_time.replace(hour=event_datetime.hour + 1)
                events.append({
                    "title": title,
                    "description": "Extracted from OCR text",
                    "start_time": event_datetime.isoformat(),
                    "end_time": end_time.isoformat() if event_datetime.hour is not None else event_datetime.isoformat()
                })
    return events
