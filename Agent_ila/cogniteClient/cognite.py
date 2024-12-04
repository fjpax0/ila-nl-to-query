import os
from dotenv import load_dotenv
from cognite.client import CogniteClient, ClientConfig, global_config
from cognite.client.credentials import OAuthClientCredentials




class CogniteClientSingleton:
    """initialize the Cognite client as a singleton

    Raises:
        ValueError: _description_

    Returns:
        _type_: congite client instance
    """
    # Class-level constants
    CDF_CLUSTER = "api"
    BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
    COGNITE_PROJECT ="welldelivery-demo"
    TENANT_ID = "d4f21b24-81a6-4563-af51-5d8c9b7301bf"
    CLIENT_ID = "ad5e6626-2465-4b2e-a561-b126e2d27153"

    _instance = None

    @staticmethod
    def _get_env_var(name):
        """Fetch and validate an environment variable."""
        value = os.environ.get(name)
        if not value:
            raise ValueError(f"Environment variable '{name}' is not set.")
        return value

    @staticmethod
    def get_instance():
        """Static method to get the Cognite client instance."""
        if CogniteClientSingleton._instance is None:
            CogniteClientSingleton._instance = CogniteClientSingleton._initialize_client()
        return CogniteClientSingleton._instance

    @staticmethod
    def _initialize_client():
        """Initialize the Cognite client."""
        client_secret = CogniteClientSingleton._get_env_var("MY_CLIENT_SECRET")
        
        creds = OAuthClientCredentials(
            token_url=f"https://login.microsoftonline.com/{CogniteClientSingleton.TENANT_ID}/oauth2/v2.0/token",
            client_id=CogniteClientSingleton.CLIENT_ID,
            client_secret=client_secret,
            scopes=[f"{CogniteClientSingleton.BASE_URL}/.default"]
        )

        cnf = ClientConfig(
            client_name="my-special-client",
            base_url=CogniteClientSingleton.BASE_URL,
            project=CogniteClientSingleton.COGNITE_PROJECT,
            credentials=creds
        )

        global_config.default_client_config = cnf
        return CogniteClient()

# Convenience function to access the Singleton instance
def get_cognite_client():
    """initialize the Cognite client as a singleton

    Returns:
        _type_: _description_
    """
    return CogniteClientSingleton.get_instance()
