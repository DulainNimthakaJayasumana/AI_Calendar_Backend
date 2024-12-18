from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from app.config import settings

# Simulated in-memory storage for tokens (use a database in production)
user_tokens = {}

router = APIRouter()

@router.get("/auth/login")
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        prompt='consent',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

@router.get("/auth/callback")
def callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Store credentials (in-memory; use a database for real applications)
    user_tokens["user"] = {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
    }
    return {"message": "Authorization successful. Tokens stored."}

def insert_event_into_google_calendar(event_data: dict):
    # Retrieve tokens
    token_info = user_tokens.get("user")
    if not token_info:
        raise HTTPException(status_code=403, detail="User not authenticated")

    creds = Credentials(
        token=token_info.get("access_token"),
        refresh_token=token_info.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET
    )
    service = build("calendar", "v3", credentials=creds)
    event_body = {
        "summary": event_data["title"],
        "description": event_data.get("description", ""),
        "start": {"dateTime": event_data["start_time"], "timeZone": "UTC"},
        "end": {"dateTime": event_data["end_time"], "timeZone": "UTC"},
    }
    created_event = service.events().insert(calendarId="primary", body=event_body).execute()
    return created_event
