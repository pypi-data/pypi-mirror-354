from ..client import BaseClient
from typing import Dict, Any

class ApiClient(BaseClient):
    def get_flux_image(self, prompt: str) -> Dict[str, Any]:
        return self._make_request('GET', '/flux', params={'p': prompt})
