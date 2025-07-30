from ..client import BaseClient
from typing import Dict, Any

class ApiClient(BaseClient):
    def bypass_link(self, url_to_bypass: str) -> Dict[str, Any]:
        return self._make_request('GET', '/bypass', params={'url': url_to_bypass})
