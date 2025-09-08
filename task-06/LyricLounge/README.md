# **LyricLounge - Your Ultimate Music Discord Bot!**

In the vast realm of music enthusiasts, where melodies unfold like epic symphonies, there is always a group of avid music lovers yearning for a seamless way to discover lyrics, track information, and musical recommendations. Enter the world of Discord bots, where code meets creativity. Fueled by passion for music discovery, this project embarks on a mission to create the ultimate Discord music companion – "LyricLounge." With its unrivaled ability to fetch lyrics, track details, and curated recommendations, "LyricLounge" becomes the heartbeat of music discussions worldwide and a loyal companion to music fans during every listening session.

## **Guiding Principles**
* Utilizes multiple music APIs to provide comprehensive music information
* Implements proper async/await patterns for optimal performance
* Provides error handling and timeout management for reliable service
* Uses Discord embeds for rich, visually appealing responses

## **Primary Features**

The bot includes several core commands for music discovery and management:

### **Core Commands**
* `/lyrics <song> - <artist>` - Fetches and displays song lyrics
* `/track <song> - <artist>` - Gets detailed track information including album, duration, and tags
* `/playlist [add/remove/view/clear] [song]` - Manage your personal playlist
* `/help` -  for getting a list of the commands along with their description.

### **Bonus Features**
* `/trending` - Shows the current top 10 trending tracks
* `/recommend <genre>` - Provides music recommendations based on genre
* `/mood <mood>` - Suggests songs based on your current mood

### **Response Features**
When commands are executed, the bot provides:
* **Lyrics**: Full song lyrics with proper formatting and chunking for long texts
* **Track Info**: Artist, album, duration, release date, and genre tags
* **Playlist Management**: Personal playlist creation and management

## **Technical Architecture**

### **APIs Used**
* **MusicBrainz API** - For comprehensive track and artist information
* **LRCLib API** - For fetching song lyrics

### APIs for Bonus Features
* **Deezer API** - For trending charts and music discovery
* **Last.fm API** - For genre-based recommendations and mood-based suggestions

### **Key Components**
* **MusicAPI Class** - Handles all external API communications
* **Session Management** - Proper aiohttp session handling with timeouts
* **Error Handling** - Comprehensive error catching and user feedback
* **Async Operations** - Non-blocking API calls for better performance

## **Setup Instructions**

### **Prerequisites**
Set up a Python Virtual Environment first. This is absolutely important and you CANNOT skip it!

```bash
# Create virtual environment
python -m venv music_bot_env

# Activate virtual environment
# On Windows:
music_bot_env\Scripts\activate
# On macOS/Linux:
source music_bot_env/bin/activate
```

### **Environment Variables**
Create a `.env` file in your project directory and add:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
LASTFM_API_KEY=your_lastfm_api_key_here
```

## **Requirements**

### **Dependencies (requirements.txt)**
```txt
discord.py>=2.3.2
aiohttp>=3.8.0
python-dotenv>=1.0.0
```

## **Resources and Links**

* [Discord.py Documentation](https://discordpy.readthedocs.io/)
* [MusicBrainz API Documentation](https://musicbrainz.org/doc/MusicBrainz_API)



---

**Where every beat finds its voice and every melody discovers its story - LyricLounge transforms your Discord into a musical universe!**
