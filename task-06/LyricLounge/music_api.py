import aiohttp
import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class MusicAPI:
    def __init__(self, session: aiohttp.ClientSession, lastfm_key: str = ""):
        self.session = session
        self.lastfm_key = lastfm_key

    async def _request(self, method, url, **kwargs) -> Optional[dict]:
        try:
            async with self.session.request(method, url, **kwargs) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    logger.warning(f"HTTP {resp.status} for {url}")
        except Exception as e:
            logger.error(f"Request error {url}: {e}")
        return None

    async def get_lyrics(self, title: str, artist: str) -> Optional[dict]:
        search_url = "https://lrclib.net/api/search"
        params = {"q": f"{artist} {title}"}
        search_res = await self._request("GET", search_url, params=params)
        if not search_res:
            return None
        items = []
        if isinstance(search_res, list):
            items = search_res
        elif isinstance(search_res, dict):
            items = search_res.get("data", search_res.get("results", []))
        for item in items[:3]:
            lyrics_id = item.get("id")
            if not lyrics_id:
                continue
            lyrics_url = f"https://lrclib.net/api/get/{lyrics_id}"
            lyrics_data = await self._request("GET", lyrics_url)
            if not lyrics_data:
                continue
            text = lyrics_data.get("plainLyrics") or lyrics_data.get("plain") or lyrics_data.get("lyrics")
            if text:
                return {
                    "plain_lyrics": text,
                    "synced_lyrics": lyrics_data.get("syncedLyrics"),
                    "title": lyrics_data.get("trackName", title),
                    "artist": lyrics_data.get("artistName", artist),
                    "album": lyrics_data.get("albumName", ""),
                    "duration": lyrics_data.get("duration", 0),
                    "source": "LRCLib"
                }
        return None

    async def get_track_info(self, title: str, artist: str) -> Optional[dict]:
        base_url = "https://musicbrainz.org/ws/2/recording/"
        query = f'recording:"{title}" AND artist:"{artist}"'
        params = {"query": query, "fmt": "json", "limit": 1, "inc": "artist-credits+releases+tags"}
        data = await self._request("GET", base_url, params=params)
        if not data or not data.get("recordings"):
            return None
        rec = data["recordings"][0]
        artists = [a["artist"]["name"] for a in rec.get("artist-credit", []) if "artist" in a]
        releases = rec.get("releases", [])
        info = {
            "title": rec.get("title", title),
            "artists": [{"name": a} for a in artists],
            "duration_formatted": self._format_duration(rec.get("length")),
            "releases": [{"title": r.get("title", "")} for r in releases[:1]],
            "tags": [t["name"] for t in rec.get("tags", [])[:5]]
        }
        return info

    async def search_songs(self, query: str) -> Optional[list]:
        url = "https://api.deezer.com/search"
        params = {"q": query, "limit": 10}
        data = await self._request("GET", url, params=params)
        if not data or not data.get("data"):
            return None
        results = []
        for track in data["data"]:
            results.append({
                "title": track.get("title", ""),
                "artist": track.get("artist", {}).get("name",""),
                "duration": self._format_duration(track.get("duration", 0)*1000)
            })
        return results

    def _format_duration(self, ms: int) -> str:
        if not ms:
            return "Unknown"
        s = ms // 1000
        return f"{s//60}:{s%60:02d}"

