from requests import Session
from urllib.parse import urljoin

class BuiltAPISession(Session):
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)


def init_session(workspace_id: str, token: str, base_url: str):
    session = BuiltAPISession(base_url=base_url)
    session.headers = {
        "Authorization": f"Bearer {token}",
        "x-builtapi-workspace-id": workspace_id
    }

    return session