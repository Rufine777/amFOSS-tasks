import aiohttp
import asyncio
import logging
from typing import Optional, Dict, List, Any, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicAPI:
    def __init__(self, session: aiohttp.ClientSession, lastfm_key: str = ""):
        self.session = session
        self.lastfm_key = lastfm_key
        self.mb_headers = {
            "User-Agent": "LyricLounge/1.0 (contact@yourapp.com)",
            "Accept": "application/json"
        }
        self.request_timeout = aiohttp.ClientTimeout(total=15)

    async def _safe_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """Make a safe HTTP request with error handling"""
        try:
            kwargs.setdefault('timeout', self.request_timeout)
            async with self.session.request(method, url, **kwargs) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 429:  # Rate limited
                    logger.warning(f"Rate limited by {url}")
                    await asyncio.sleep(1)
                    return None
                else:
                    logger.warning(f"HTTP {resp.status} from {url}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout requesting {url}")
            return None
        except Exception as e:
            logger.error(f"Error requesting {url}: {e}")
            return None

    async def lrclib_search(self, title: str, artist: str = None) -> Optional[List[Dict]]:
        """Search for lyrics on LRCLIB with robust response handling"""
        query = f"{artist} {title}" if artist else title
        url = "https://lrclib.net/api/search"
        params = {"q": query.strip()}
        
        logger.info(f"Searching LRCLIB for: {query}")
        data = await self._safe_request("GET", url, params=params)
        
        if not data:
            return None
            
        # Handle different response formats
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("data", data.get("results", []))
        else:
            logger.warning(f"Unexpected LRCLIB search response format: {type(data)}")
            return None

    async def lrclib_get(self, lrclib_id: int) -> Optional[Dict]:
        """Get specific lyrics by ID from LRCLIB"""
        url = f"https://lrclib.net/api/get/{lrclib_id}"
        logger.info(f"Fetching lyrics ID {lrclib_id}")
        return await self._safe_request("GET", url)

    async def get_lyrics(self, title: str, artist: str = None) -> Optional[Dict]:
        """Get lyrics with comprehensive error handling and format detection"""
        try:
            # Search for the song
            search_results = await self.lrclib_search(title, artist)
            if not search_results:
                logger.info(f"No search results for: {title} - {artist}")
                return None

            # Try multiple matches for better accuracy
            for i, result in enumerate(search_results[:3]):  # Check top 3 results
                if not isinstance(result, dict):
                    continue
                    
                lyrics_id = result.get("id")
                if not lyrics_id:
                    continue
                
                logger.info(f"Trying result {i+1}: {result.get('artistName', 'Unknown')} - {result.get('trackName', 'Unknown')}")
                
                # Get full lyrics data
                lyrics_data = await self.lrclib_get(lyrics_id)
                if lyrics_data:
                    # Process and validate lyrics
                    processed = self._process_lyrics(lyrics_data)
                    if processed:
                        return processed
                        
                # Small delay between requests to be respectful
                if i < len(search_results) - 1:
                    await asyncio.sleep(0.5)
            
            logger.info("No valid lyrics found in any results")
            return None
            
        except Exception as e:
            logger.error(f"Error in get_lyrics: {e}")
            return None

    def _process_lyrics(self, lyrics_data: Dict) -> Optional[Dict]:
        """Process and validate lyrics data"""
        if not isinstance(lyrics_data, dict):
            return None
            
        # Extract different lyrics formats
        lyrics_text = None
        synced_lyrics = None
        
        # Check for various lyrics fields
        for field in ['plainLyrics', 'plain', 'lyrics', 'unsynced']:
            if lyrics_data.get(field):
                lyrics_text = lyrics_data[field]
                break
                
        for field in ['syncedLyrics', 'synced', 'lrc']:
            if lyrics_data.get(field):
                synced_lyrics = lyrics_data[field]
                break
        
        # Ensure we have some lyrics
        if not lyrics_text and not synced_lyrics:
            return None
            
        # Build comprehensive response
        result = {
            'title': lyrics_data.get('trackName', lyrics_data.get('name', '')),
            'artist': lyrics_data.get('artistName', lyrics_data.get('artist', '')),
            'album': lyrics_data.get('albumName', lyrics_data.get('album', '')),
            'duration': lyrics_data.get('duration', 0),
            'plain_lyrics': lyrics_text,
            'synced_lyrics': synced_lyrics,
            'has_synced': bool(synced_lyrics),
            'source': 'LRCLIB',
            'id': lyrics_data.get('id'),
            'raw_data': lyrics_data
        }
        
        return result

    async def get_track_info(self, title: str, artist: str = None) -> Optional[Dict]:
        """Get track metadata from MusicBrainz with enhanced search"""
        try:
            # Build search query
            query_parts = []
            if title:
                query_parts.append(f'recording:"{title}"')
            if artist:
                query_parts.append(f'artist:"{artist}"')
                
            if not query_parts:
                return None
                
            query = " AND ".join(query_parts)
            url = "https://musicbrainz.org/ws/2/recording/"
            params = {
                "query": query,
                "fmt": "json",
                "limit": 5,
                "inc": "artist-credits+releases+genres+tags+ratings"
            }
            
            logger.info(f"Searching MusicBrainz for: {query}")
            result = await self._safe_request("GET", url, params=params, headers=self.mb_headers)
            
            if not result or not result.get("recordings"):
                return None
                
            # Process the best match
            recording = result["recordings"][0]
            
            # Extract comprehensive track info
            track_info = {
                'title': recording.get("title", "Unknown"),
                'mb_id': recording.get("id"),
                'duration_ms': recording.get("length"),
                'duration_formatted': self._format_duration(recording.get("length")),
                'artists': [],
                'releases': [],
                'genres': [],
                'tags': [],
                'country': None,
                'date': None,
                'score': recording.get("score", 0)
            }
            
            # Extract artists
            if recording.get("artist-credit"):
                for credit in recording["artist-credit"]:
                    if isinstance(credit, dict) and credit.get("artist"):
                        track_info['artists'].append({
                            'name': credit["artist"]["name"],
                            'id': credit["artist"]["id"],
                            'sort_name': credit["artist"].get("sort-name", "")
                        })
            
            # Extract releases (albums)
            if recording.get("releases"):
                for release in recording["releases"][:3]:  # Top 3 releases
                    release_info = {
                        'title': release.get("title", "Unknown"),
                        'id': release.get("id"),
                        'date': release.get("date", ""),
                        'country': release.get("country", ""),
                        'status': release.get("status", "")
                    }
                    track_info['releases'].append(release_info)
                    
                    # Set primary release info
                    if not track_info['date'] and release.get("date"):
                        track_info['date'] = release["date"]
                    if not track_info['country'] and release.get("country"):
                        track_info['country'] = release["country"]
            
            # Extract genres and tags
            for tag in recording.get("tags", []):
                track_info['tags'].append(tag.get("name", ""))
            
            return track_info
            
        except Exception as e:
            logger.error(f"Error in get_track_info: {e}")
            return None

    def _format_duration(self, duration_ms: Optional[int]) -> str:
        """Format duration from milliseconds to MM:SS"""
        if not duration_ms:
            return "Unknown"
        
        try:
            seconds = int(duration_ms) // 1000
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}:{seconds:02d}"
        except (ValueError, TypeError):
            return "Unknown"

    async def get_trending_tracks(self, limit: int = 10) -> List[Dict]:
        """Get trending tracks from Deezer charts"""
        try:
            url = f"https://api.deezer.com/chart/0/tracks"
            params = {"limit": min(limit, 50)}  # Max 50
            
            data = await self._safe_request("GET", url, params=params)
            if not data or not data.get("data"):
                return []
            
            tracks = []
            for track in data["data"]:
                track_info = {
                    'title': track.get("title", "Unknown"),
                    'artist': track.get("artist", {}).get("name", "Unknown"),
                    'album': track.get("album", {}).get("title", "Unknown"),
                    'duration': track.get("duration", 0),
                    'preview_url': track.get("preview", ""),
                    'deezer_id': track.get("id"),
                    'rank': track.get("position", 0)
                }
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error getting trending tracks: {e}")
            return []

    async def search_artist_top_tracks(self, artist: str, limit: int = 10) -> List[Dict]:
        """Search for an artist's top tracks using Deezer"""
        try:
            # First search for the artist
            search_url = "https://api.deezer.com/search/artist"
            params = {"q": artist, "limit": 1}
            
            data = await self._safe_request("GET", search_url, params=params)
            if not data or not data.get("data"):
                return []
            
            artist_id = data["data"][0].get("id")
            if not artist_id:
                return []
            
            # Get artist's top tracks
            tracks_url = f"https://api.deezer.com/artist/{artist_id}/top"
            params = {"limit": min(limit, 50)}
            
            tracks_data = await self._safe_request("GET", tracks_url, params=params)
            if not tracks_data or not tracks_data.get("data"):
                return []
            
            tracks = []
            for track in tracks_data["data"]:
                track_info = {
                    'title': track.get("title", "Unknown"),
                    'artist': track.get("artist", {}).get("name", "Unknown"),
                    'album': track.get("album", {}).get("title", "Unknown"),
                    'duration': self._format_duration(track.get("duration", 0) * 1000),
                    'rank': track.get("rank", 0),
                    'deezer_id': track.get("id")
                }
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error searching artist top tracks: {e}")
            return []

    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
