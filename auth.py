import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY")  # read from environment

def verify_api_key(x_api_key: str = Header(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server API key not configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
