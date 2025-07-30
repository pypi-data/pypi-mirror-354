import os
import json
from functools import lru_cache

from dotenv import load_dotenv
from google.cloud import secretmanager

# new import to auto-discover your project
import google.auth

load_dotenv()

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

def validate_api_key(api_key: str):
    valid = _load_valid_keys()
    if not api_key or api_key not in valid:
        raise ValueError("Invalid or missing API Key")
    return api_key