from ..client import BaseClient
from typing import Dict, Any, Optional

class ApiClient(BaseClient):
    def get_quote(self, category: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if category:
            params['c'] = category
        return self._make_request('GET', '/quote', params=params)

    def get_key_info(self, key_to_check: Optional[str] = None) -> Dict[str, Any]:
        target_key = key_to_check or self._parent.api_key
        if not target_key:
            from ..client import APIError
            raise APIError("No API key provided to check.", 400)
        return self._make_request(
            'GET', '/key-info', params={'key': target_key}, send_key=False
        )

    def get_gag_stock(self) -> Dict[str, Any]:
        return self._make_request('GET', '/gagstock')
