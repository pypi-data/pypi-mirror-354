from ..client import BaseClient
from typing import Dict, Any, Optional

class ApiClient(BaseClient):
    def get_flux_image(self, prompt: str) -> Dict[str, Any]:
        """
        Generates an image using the Flux AI model.

        Args:
            prompt: The text description for the image.

        Returns:
            A dictionary containing the image URL.
        """
        return self._make_request('GET', '/flux', params={'p': prompt})

    def generate_qr_code(self, data: str, qr_type: str = 'url') -> Dict[str, Any]:
        """
        Generates a QR code.

        Args:
            data: The content to encode in the QR code.
            qr_type: The type of QR code (e.g., 'url', 'text', 'wifi'). See API docs for all types.

        Returns:
            A dictionary containing the QR code image URL.
        """
        params = {'data': data}
        return self._make_request('GET', f'/qr/{qr_type}', params=params)

    def generate_rankcard(
        self,
        username: str,
        avatar: str,
        current_xp: int,
        next_level_xp: int,
        level: int,
        rank: int,
        previous_level_xp: Optional[int] = None,
        custom_bg_url: Optional[str] = None,
        xp_color_hex: Optional[str] = None,
        circle_avatar: bool = False
    ) -> bytes:
        """
        Generates a Discord-style rank card image.

        Args:
            username: The user's name.
            avatar: URL to the user's avatar.
            current_xp: The user's current XP.
            next_level_xp: The XP needed for the next level.
            level: The user's level.
            rank: The user's rank.
            previous_level_xp: XP of the previous level (optional).
            custom_bg_url: URL for a custom background image (optional).
            xp_color_hex: Hex code for the XP bar color (e.g., 'FFFFFF', optional).
            circle_avatar: Whether to use a circular avatar (optional, default False).

        Returns:
            The raw image data in bytes.
        """
        params = {
            'username': username,
            'avatar': avatar,
            'currentXp': current_xp,
            'nextLevelXp': next_level_xp,
            'level': level,
            'rank': rank,
            'circleAvatar': str(circle_avatar).lower()
        }
        if previous_level_xp is not None:
            params['previousLevelXp'] = previous_level_xp
        if custom_bg_url:
            params['customBg'] = custom_bg_url
        if xp_color_hex:
            params['xpColor'] = xp_color_hex.lstrip('#')
            
        return self._make_binary_request('GET', '/rankcard', params=params)
