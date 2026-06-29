from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="api-key",
    auto_error=False
)

def get_api_key(
    api_key: str = Security(api_key_header)
):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    return api_key