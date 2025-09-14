# Task 06
# Discord Music & Lyrics Bot 🎵

This is a custom-built Discord bot that combines **music discovery**, **lyrics fetching**, and **user statistics tracking** into one cohesive project. It was designed with a modular approach to keep the code clean, extensible, and easy to maintain.

---

## Project Structure

- **`bot.py`**  
  The heart of the bot. Handles:
  - Discord connection & slash commands  
  - User interaction (help, search, lyrics, stats)  
  - Reading/writing user activity to `user_stats.json`  
  - Connecting to `music_api.py` for API calls  

- **`music_api.py`**  
  A dedicated API layer that abstracts external services.  
  - **LRCLib API** → Fetches lyrics  
  - **MusicBrainz API** → Retrieves artist & album metadata  
  - **Deezer API** → Finds track details and previews  
  - (Optional) **Last.fm API** → Can be integrated for track scrobbling or recommendations  

- **`user_stats.json`**  
  Stores user-level statistics in JSON format:  
  - Number of commands used  
  - Favorite command  
  - Last used timestamp  
  - Per-command breakdown  

- **`playlist.json`**  
  Placeholder file for playlist functionality (currently empty).  
  Can be extended later to save user-created playlists.

---

## How the Files Work Together

1. A user runs a slash command (e.g., `/lyrics` or `/search`) in Discord.  
2. `bot.py` receives the command → sends a request to **`music_api.py`**.  
3. `music_api.py` calls the appropriate API (LRCLib, Deezer, MusicBrainz) and returns structured results.  
4. `bot.py` formats the results and replies back in Discord.  
5. User activity is logged into **`user_stats.json`** for future stats tracking.  

This modular design ensures:
- **Separation of concerns** (Discord logic vs. API logic vs. storage).  
- Easy debugging (problems in APIs stay in `music_api.py`).  
- Easy to scale (more commands or APIs can be added).  

---

## Commands Implemented

- **`/help`** → Lists all available commands.  
- **`/search <track>`** → Searches for a song and returns metadata (artist, album, link).  
- **`/lyrics <track>`** → Fetches lyrics from LRCLib.  
- **`/stats`** → Displays user-specific bot usage statistics.  

---

## Services Used

- **[Discord.py](https://discordpy.readthedocs.io/)** → To interact with Discord via slash commands.  
- **[aiohttp](https://docs.aiohttp.org/)** → For asynchronous HTTP requests to APIs.  
- **[LRCLib API](https://lrclib.net/)** → Lyrics retrieval.  
- **[MusicBrainz API](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2)** → Artist & album info.  
- **[Deezer API](https://developers.deezer.com/api)** → Track metadata and previews.  
- *(Optional)* **[Last.fm API](https://www.last.fm/api)** → For advanced features like scrobbling or recommendations.  

---

## My Approach

- **Why modularize?**  
  To keep the bot organized — Discord logic in one file, API logic in another, and data storage separate.  

- **Why JSON for storage?**  
  Simple, lightweight, and human-readable. A database could be used later for scaling, but JSON is perfect for MVP.  

- **Why multiple APIs?**  
  No single API provides everything:
  - LRCLib for lyrics  
  - Deezer for track metadata  
  - MusicBrainz for structured artist/album info  

- **Alternatives considered:**  
  - Could have used a database (SQLite/Postgres) → but JSON was simpler.  
  - Could have used one API (e.g., Spotify API) → but requires OAuth and is more complex for a small project.  
  - Prefix commands (`!help`) → but slash commands provide a cleaner modern experience.  

---

## Inspiration

Resources like **W3Schools**, API documentation, and Discord developer docs were heavily used during development.

---
## Steps to Run

1. Clone this repository and make sure you are inside the `LyricLounge` directory.  
2. Create a virtual environment:  
   ```bash
   python3 -m venv music_bot_env/ 
   ```
3. Activate the environment:
```bash
source music_bot_env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the bot:
```bash
python3 bot.py
```