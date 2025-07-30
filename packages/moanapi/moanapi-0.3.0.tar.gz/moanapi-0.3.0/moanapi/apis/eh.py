from ..client import BaseClient
from typing import Dict, Any

class ApiClient(BaseClient):
    def get_server_details(self, server_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'/eh/{server_id}')
        
    def search_servers(self, query: str) -> Dict[str, Any]:
        return self._make_request('GET', f'/eh/search/{query}')
