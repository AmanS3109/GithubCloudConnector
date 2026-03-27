from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/login")
async def login_via_github():
    """Redirects the user to GitHub to authorize the app."""
    # We request the 'repo' scope so the token has permission to read/write issues and PRs
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={settings.github_client_id}&scope=repo"
    return RedirectResponse(github_auth_url)

@router.get("/callback")
async def github_callback(code: str):
    """Catches the callback from GitHub and exchanges the code for an access token."""
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    payload = {
        "client_id": settings.github_client_id,
        "client_secret": settings.github_client_secret,
        "code": code
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, json=payload, headers=headers)
        data = response.json()
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error_description"])
        
        return {
            "message": "Authentication successful!",
            "access_token": data.get("access_token"),
            "instructions": "Copy this access_token. Go to /docs, click the 'Authorize' padlock, and paste it to use the API."
        }