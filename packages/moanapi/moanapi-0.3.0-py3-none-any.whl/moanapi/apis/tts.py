from ..client import BaseClient
from typing import Dict, Any

class ApiClient(BaseClient):
    def get_help(self) -> Dict[str, Any]:
        return self._make_request('GET', '/tts/help', send_key=False)
        
    def generate(self, text: str, voice: str = 'en-us', speed: int = 160, pitch: int = 50) -> Dict[str, Any]:
        params = {
            'text': text,
            'voice': voice,
            'speed': speed,
            'pitch': pitch
        }
        return self._make_request('GET', '/tts/generate', params=params)
