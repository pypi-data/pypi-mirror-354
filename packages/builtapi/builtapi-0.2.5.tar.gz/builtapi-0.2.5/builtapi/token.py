import requests

import builtapi.settings as settings


def get_token(username: str = None, password: str = None,
              client_id: str = None, client_secret: str = None,
              audience: str = None, token_url: str = None) -> str:
    """
    Obtain access token

    NB: Parameters "client_id" and "client_secret" are the same for all username and password
    """
    username = username or settings.BUILTAPI_CLIENT_USER
    password = password or settings.BUILTAPI_CLIENT_PASSWORD
    client_id = client_id or settings.BUILTAPI_CLIENT_ID
    client_secret = client_secret or settings.BUILTAPI_CLIENT_SECRET
    audience = audience or settings.BUILTAPI_AUDIENCE
    token_url = token_url or settings.BUILTAPI_TOKEN_URL

    required_fields = {
        "username": username,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience,
    }

    missing_fields = [field for field, value in required_fields.items() if value is None]

    if missing_fields:
        raise ValueError(f"The following fields cannot be None to generate token: {', '.join(missing_fields)}")

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "audience": audience,
        "scope": "openid profile email",
        "grant_type": "password"
    }
    response = requests.post(token_url, data=body)
    response.raise_for_status()
    response = response.json()
    return response['access_token']
