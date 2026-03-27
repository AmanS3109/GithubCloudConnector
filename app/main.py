from fastapi import FastAPI
from app.routers import github, auth

app = FastAPI(
    title="GitHub Cloud Connector",
    description="An API to interact securely with GitHub using OAuth 2.0",
    version="1.0.0"
)

# Connect both routers to the main app
app.include_router(auth.router)
app.include_router(github.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "GitHub OAuth Connector is running!",
        "auth_flow": "Navigate to http://127.0.0.1:8000/auth/login to authenticate."
    }