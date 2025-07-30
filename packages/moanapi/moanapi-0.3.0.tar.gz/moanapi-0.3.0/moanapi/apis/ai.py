from ..client import BaseClient
from typing import Dict, Any, Optional

class ApiClient(BaseClient):
    def girlfriend_chat(self, name: str, message: str, gf_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Chat with an AI-powered virtual girlfriend.

        Args:
            name: Your name.
            message: The message to send to her.
            gf_name: Her name (optional, defaults to 'Mia').

        Returns:
            A dictionary containing the AI's response.
        """
        params = {
            'name': name,
            'message': message,
        }
        if gf_name:
            params['gf-name'] = gf_name
        return self._make_request('GET', '/ai/gf', params=params)
