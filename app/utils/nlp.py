import spacy
import dateparser

nlp = spacy.load("en_core_web_sm")

def extract_events_from_text(text: str):
    doc = nlp(text)
    events = []
    event_keywords = ["class", "lecture", "meeting", "event", "appointment"]

    for sent in doc.sents:
        sentence_text = sent.text.strip().lower()
        if any(keyword in sentence_text for keyword in event_keywords):
            event_datetime = dateparser.parse(sentence_text, settings={"PREFER_DATES_FROM": "future"})
            if not event_datetime:
                continue

            entities = {ent.label_: ent.text for ent in sent.ents}
            title = entities.get("ORG") or entities.get("PERSON") or "Scheduled Event"

            end_time = event_datetime.replace(hour=event_datetime.hour + 1)
            events.append({
                "title": title,
                "description": sentence_text,
                "start_time": event_datetime.isoformat(),
                "end_time": end_time.isoformat(),
            })
    return events
