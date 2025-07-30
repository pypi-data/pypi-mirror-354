import os
import json
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from google.cloud import secretmanager
from starlette.status import HTTP_401_UNAUTHORIZED

# new import to auto-discover your project
import google.auth

load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@lru_cache(maxsize=1)
def _load_valid_keys() -> set[str]:
    # first, try the env-var
    proj = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not proj:
        # fall back to application default credentials
        _, proj = google.auth.default()
    secret_id = os.environ["API_KEYS_SECRET_NAME"]
    version   = os.getenv("API_KEYS_SECRET_VERSION", "latest")

    client = secretmanager.SecretManagerServiceClient()
    name   = f"projects/{proj}/secrets/{secret_id}/versions/{version}"
    payload = client.access_secret_version(request={"name": name}).payload.data.decode("utf-8")

    try:
        raw = json.loads(payload)
        keys = set(raw) if isinstance(raw, list) else {str(raw)}
    except json.JSONDecodeError:
        parts = [p.strip() for p in payload.replace("\n",",").split(",")]
        keys = {p for p in parts if p}
    return keys

async def validate_api_key(api_key: str = Security(api_key_header)):
    valid = _load_valid_keys()
    if not api_key or api_key not in valid:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key