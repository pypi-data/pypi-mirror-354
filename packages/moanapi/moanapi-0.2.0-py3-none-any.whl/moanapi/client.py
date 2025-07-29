import requests
import pkgutil
import importlib
from typing import Optional, Dict, Any
from . import apis
# REMOVED: from . import __version__

class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(f"[MoanAPI Error] Status {status_code}: {message}" if status_code else f"[MoanAPI Error] {message}")

def _check_for_updates():
    # ADDED IMPORT HERE
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
    print("--- Moan API Python Module Help ---")
    print("\nThis module provides a simple, object-oriented interface to the Moan API.\n")
    print("1. Initialization:")
    print("   client = moanapi.Client(api_key='YOUR_API_KEY')\n")
    print("2. Usage:")
    print("   - client.roblox.get_user_info(user_id=1)")
    print("   - client.utility.get_quote(category='anime')\n")
    print("3. Available API Endpoints:")
    
    try:
        response = requests.get("https://moanapi.ddns.net/api/apis.json", timeout=10)
        response.raise_for_status()
        endpoints = response.json()
        
        print("   " + "="*40)
        for api in sorted(endpoints, key=lambda x: x['name']):
            print(f"   - {api['name']:<30} | Example: {api['url']}")
        print("   " + "="*40)
    except requests.RequestException as e:
        print(f"\n   Could not fetch the live API list. Error: {e}")
    print("\n-------------------------------------\n")


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

class Client:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://moanapi.ddns.net/api"
        self._load_api_modules()

    def _load_api_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(apis.__path__, apis.__name__ + "."):
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'ApiClient'):
                    attr_name = module_name.split('.')[-1]
                    setattr(self, attr_name, module.ApiClient(self))
            except Exception as e:
                print(f"Warning: Could not load API module '{module_name}': {e}")
