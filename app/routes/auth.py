from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from app.config import settings

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

    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None
    }
