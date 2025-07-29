import aiohttp
from typing import Any, Optional, Dict, Union

class GDBAsync:
    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.api: str = "https://gdbrowser.com/api"
        self.session: Optional[aiohttp.ClientSession] = session
        self._own_session: bool = False

    async def _ensure_session(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
            self._own_session = True

    async def _get(
        self, endpoint: str, is_json: bool = True
    ) -> Union[Dict[str, Any], str]:
        await self._ensure_session()
        url = f"{self.api}/{endpoint}"
        async with self.session.get(url) as response:
            if is_json:
                return await response.json()
            return await response.text()

    async def close(self) -> None:
        if self._own_session and self.session and not self.session.closed:
            await self.session.close()

    async def get_level(self, level_id: int, download: bool = False) -> Dict[str, Any]:
        suffix = "?download" if download else ""
        return await self._get(f"level/{level_id}{suffix}")

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        return await self._get(f"profile/{username}")

    async def get_leaderboard(
        self, count: int = 100, is_creator: bool = False
    ) -> Dict[str, Any]:
        suffix = f"?count={count}"
        if is_creator:
            suffix += "&creator"
        return await self._get(f"leaderboard{suffix}")

    async def get_map_packs(self) -> Dict[str, Any]:
        return await self._get("mappacks")

    async def get_gauntlets_list(self) -> Dict[str, Any]:
        return await self._get("gauntlets")

    async def get_level_leaderboard(
        self, level_id: int, count: int = 100
    ) -> Dict[str, Any]:
        return await self._get(f"leaderboardLevel/{level_id}?count={count}")

    async def get_user_posts(
        self,
        user_id: int,
        page: int = 0,
        count: int = 10,
        type: str = "profile"
    ) -> Dict[str, Any]:
        return await self._get(f"comments/{user_id}?page={page}&count={count}&type={type}")

    async def check_song_verification(self, song_id: int) -> str:
        return await self._get(f"song/{song_id}", is_json=False)

    async def analyze_level(self, level_id: int) -> Dict[str, Any]:
        return await self._get(f"analyze/{level_id}")

    async def get_user_icon(
        self,
        username: str,
        form: str = "cube",
        size: str = "auto"
    ) -> Dict[str, Any]:
        return await self._get(f"icon/{username}?form={form}&size={size}")
