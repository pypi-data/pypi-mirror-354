from ..client import BaseClient
from typing import Dict, Any

class ApiClient(BaseClient):
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/user-info/{user_id}')

    def get_username_history(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/username-history/{user_id}')

    def get_user_presence(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/presence/{user_id}')
        
    def get_friends(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/friends/{user_id}')

    def get_friend_follower_counts(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/friend-follower-counts/{user_id}')

    def get_avatar_details(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/avatar-details/{user_id}')

    def get_currently_wearing(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/currently-wearing/{user_id}')

    def get_user_groups(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/user-groups/{user_id}')

    def get_user_badges(self, user_id: int) -> Dict[str, Any]:
        return self._make_request('GET', f'/roblox/user-badges/{user_id}')
