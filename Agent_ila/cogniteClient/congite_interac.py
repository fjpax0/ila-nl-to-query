import os
from pathlib import Path
from tempfile import gettempdir
import atexit
from typing import Any
from msal import PublicClientApplication, SerializableTokenCache
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials, Token

# Constants
TENANT_ID = "d4f21b24-81a6-4563-af51-5d8c9b7301bf"
CLIENT_ID = "ad5e6626-2465-4b2e-a561-b126e2d27153"
CDF_CLUSTER = "api"
COGNITE_PROJECT = "welldelivery-demo"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
SCOPES = [f"{BASE_URL}/.default"]
AUTHORITY_URI = f"https://login.microsoftonline.com/{TENANT_ID}"
CACHE_PATH = Path(gettempdir()) / "cognite_auth_cache"

app = None  # MSAL application instance (global)


def create_cache(path: Path) -> SerializableTokenCache:
    """Create a persistent token cache."""
    cache = SerializableTokenCache()
    if path.exists():
        cache.deserialize(path.read_text())
    atexit.register(lambda: path.write_text(cache.serialize()) if cache.has_state_changed else None)
    return cache


def authenticate_azure() -> dict[str, Any]:
    """Authenticate with Azure using MSAL for interactive authentication."""
    global app
    if app is None:
        app = PublicClientApplication(
            client_id=CLIENT_ID, authority=AUTHORITY_URI, token_cache=create_cache(CACHE_PATH)
        )
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        result = None  # Ensure 'result' is defined here
    
    if not result:
        result = app.acquire_token_interactive(scopes=SCOPES)
    return result


def get_client(interactive: bool = False, cdf_version= None) -> CogniteClient:
    """Get a CogniteClient instance."""
    if interactive:
        creds = authenticate_azure()
        credentials = Token(creds["access_token"])
    else:
        credentials = OAuthClientCredentials(
            token_url=f"{AUTHORITY_URI}/oauth2/v2.0/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=SCOPES,
        )
    if cdf_version is not None:
        config = ClientConfig(
            project=COGNITE_PROJECT,
            credentials=credentials,
            headers={"cdf-version": cdf_version},
            base_url=BASE_URL,
            client_name="well_delivery_demo",
        )
    else:
        config = ClientConfig(
            project=COGNITE_PROJECT,
            credentials=credentials,
            base_url=BASE_URL,
            client_name="well_delivery_demo",
        )
    return CogniteClient(config)
