import requests
import pkgutil
import importlib
from typing import Optional, Dict, Any
from . import apis

class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(f"[MoanAPI Error] Status {status_code}: {message}" if status_code else f"[MoanAPI Error] {message}")

def _check_for_updates():
    from . import __version__
    try:
        response = requests.get("https://pypi.org/pypi/moanapi/json", timeout=3)
        if response.status_code == 200:
            latest_version = response.json()['info']['version']
            if latest_version > __version__:
                print("="*60)
                print(f"UPDATE AVAILABLE: You are using moanapi version {__version__}.")
                print(f"Version {latest_version} is available.")
                print("Upgrade now by running: pip install --upgrade moanapi")
                print("="*60 + "\n")
    except requests.RequestException:
        pass

def help():
    _check_for_updates()
    
    usage_info = [
        {'module': 'ai', 'call': 'girlfriend_chat(name="Alex", message="Hey!")', 'desc': 'Chat with an AI girlfriend.'},
        {'module': 'bypass', 'call': 'bypass_link(url_to_bypass="http://...")', 'desc': 'Bypass ad-links.'},
        {'module': 'eh', 'call': 'get_server_details(server_id="...")', 'desc': 'Get details for a specific EH server.'},
        {'module': 'eh', 'call': 'search_servers(query="RP")', 'desc': 'Search for an Emergency Hamburg server.'},
        {'module': 'generative', 'call': 'get_flux_image(prompt="a cat wizard")', 'desc': 'Generate an image using Flux AI.'},
        {'module': 'generative', 'call': 'generate_qr_code(qr_type="url", data="...")', 'desc': 'Generate a QR code image URL.'},
        {'module': 'generative', 'call': 'generate_rankcard(username="User", ...)', 'desc': 'Generate a rank card (returns image bytes).'},
        {'module': 'roblox', 'call': 'get_avatar_details(user_id=1)', 'desc': "Get a user's avatar details."},
        {'module': 'roblox', 'call': 'get_currently_wearing(user_id=1)', 'desc': 'Get asset IDs a user is wearing.'},
        {'module': 'roblox', 'call': 'get_friend_follower_counts(user_id=1)', 'desc': 'Get friend, follower, and following counts.'},
        {'module': 'roblox', 'call': 'get_friends(user_id=1)', 'desc': "Get a user's friends list."},
        {'module': 'roblox', 'call': 'get_user_badges(user_id=1)', 'desc': "Get a user's badges."},
        {'module': 'roblox', 'call': 'get_user_groups(user_id=1)', 'desc': "Get a user's groups."},
        {'module': 'roblox', 'call': 'get_user_info(user_id=1)', 'desc': "Get a Roblox user's primary info."},
        {'module': 'roblox', 'call': 'get_user_presence(user_id=1)', 'desc': "Get a user's presence (online status)."},
        {'module': 'roblox', 'call': 'get_username_history(user_id=1)', 'desc': "Get a Roblox user's name history."},
        {'module': 'tts', 'call': 'generate(text="hello", voice="en-us")', 'desc': 'Generate a TTS audio file URL.'},
        {'module': 'tts', 'call': 'get_help()', 'desc': 'Get available TTS voices.'},
        {'module': 'utility', 'call': 'get_gag_stock()', 'desc': 'Get Grow a Garden stock info.'},
        {'module': 'utility', 'call': 'get_key_info()', 'desc': 'Get info about your API key.'},
        {'module': 'utility', 'call': 'get_quote(category="anime")', 'desc': 'Get a random or anime quote.'},
    ]

    print("--- Moan API Python Module Help ---")
    print("\nThis module provides a simple, object-oriented interface to the Moan API.\n")
    print("1. Initialization:")
    print("   import moanapi")
    print("   moan = moanapi.Client(api_key='YOUR_API_KEY')\n")
    print("2. Available Functions:")
    
    sorted_info = sorted(usage_info, key=lambda x: (x['module'], x['call']))
    
    max_len = max(len(f"moan.{i['module']}.{i['call']}") for i in sorted_info) + 2
    
    for info in sorted_info:
        usage_string = f"moan.{info['module']}.{info['call']}"
        print(f"   {usage_string:<{max_len}} # {info['desc']}")

    print("\n-------------------------------------------------\n")


class BaseClient:
    def __init__(self, parent_client: 'Client'):
        self._parent = parent_client

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        send_key: bool = True
    ) -> Dict[str, Any]:
        if params is None:
            params = {}
        if send_key:
            if not self._parent.api_key:
                raise APIError("API key is required for this endpoint.", 401)
            params['key'] = self._parent.api_key
        url = self._parent.base_url + endpoint
        try:
            response = requests.request(method, url, params=params, timeout=45)
            if 'application/json' not in response.headers.get('Content-Type', ''):
                if 400 <= response.status_code < 600:
                    raise APIError(f"Server returned a non-JSON error page.", response.status_code)
            data = response.json()
            response.raise_for_status()
            return data
        except requests.exceptions.HTTPError as e:
            error_msg = data.get("error", "An unknown HTTP error occurred.")
            if 'details' in data:
                error_msg += f" Details: {data['details']}"
            raise APIError(error_msg, e.response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIError(f"A network error occurred: {e}")
        except ValueError:
            raise APIError("Failed to decode JSON response from the server.")

    def _make_binary_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bytes:
        if params is None:
            params = {}
        if not self._parent.api_key:
            raise APIError("API key is required for this endpoint.", 401)
        params['key'] = self._parent.api_key
        url = self._parent.base_url + endpoint
        try:
            response = requests.request(method, url, params=params, timeout=45)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = response.json()
                error_msg = data.get("error", "The server returned a JSON error instead of binary content.")
                if 'description' in data: # from abort()
                    error_msg = data['description']
                raise APIError(error_msg, response.status_code)

            return response.content
        
        except requests.exceptions.HTTPError as e:
            try:
                data = response.json()
                error_msg = data.get("error", "An unknown HTTP error occurred.")
                if 'description' in data:
                     error_msg = data['description']
                raise APIError(error_msg, e.response.status_code)
            except ValueError:
                 raise APIError(f"Server returned a non-JSON error page.", e.response.status_code)

        except requests.exceptions.RequestException as e:
            raise APIError(f"A network error occurred: {e}")

class Client:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://moanapi.ddns.net/api"
        self._load_api_modules()
        _check_for_updates()

    def _load_api_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(apis.__path__, apis.__name__ + "."):
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'ApiClient'):
                    attr_name = module_name.split('.')[-1]
                    setattr(self, attr_name, module.ApiClient(self))
            except Exception as e:
                print(f"Warning: Could not load API module '{module_name}': {e}")
