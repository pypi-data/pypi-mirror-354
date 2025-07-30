import os

BUILTAPI_CLIENT_ID = os.getenv("BUILTAPI_CLIENT_ID")
BUILTAPI_CLIENT_SECRET = os.getenv("BUILTAPI_CLIENT_SECRET")
BUILTAPI_CLIENT_USER = os.getenv("BUILTAPI_CLIENT_USER")
BUILTAPI_CLIENT_PASSWORD = os.getenv("BUILTAPI_CLIENT_PASSWORD")
BUILTAPI_AUDIENCE = os.getenv("BUILTAPI_AUDIENCE", "https://gateway.builtapi.dev")
BUILTAPI_GATEWAY_URL = os.getenv("BUILTAPI_GATEWAY_URL", "https://gateway.builtapi.dev")
BUILTAPI_TOKEN_URL = os.getenv("BUILTAPI_TOKEN_URL", "https://builtapi-dev.eu.auth0.com/oauth/token")
BUILTAPI_DEFAULT_WORKSPACE_ID = os.getenv("BUILTAPI_DEFAULT_WORKSPACE_ID")
BBUILTAPI_GATEWAY_BASE_URL = "https://gateway.builtapi.dev"
