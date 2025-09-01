import os
import json
import asyncio
import logging
import random
from datetime import datetime
from dotenv import load_dotenv
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from music_api import MusicAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
LASTFM_KEY = os.getenv("LASTFM_API_KEY", "")

# File paths
PLAYLIST_FILE = "playlists.json"
STATS_FILE = "user_stats.json"

# Helper functions for data management
def load_json_file(filename: str, default: dict = None) -> dict:
    """Load JSON file with error handling"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default or {}
    except json.JSONDecodeError:
        logger.error(f"Error reading {filename}, returning default")
        return default or {}

async def save_json_file(filename: str, data: dict):
    """Save JSON file asynchronously"""
    try:
        await asyncio.to_thread(
            lambda: open(filename, "w", encoding="utf-8").write(
                json.dumps(data, ensure_ascii=False, indent=2)
            )
        )
    except Exception as e:
        logger.error(f"Error saving {filename}: {e}")

def load_playlists():
    return load_json_file(PLAYLIST_FILE, {})

async def save_playlists(playlists):
    await save_json_file(PLAYLIST_FILE, playlists)

def load_user_stats():
    return load_json_file(STATS_FILE, {})

async def save_user_stats(stats):
    await save_json_file(STATS_FILE, stats)

async def update_user_stats(user_id: str, command: str):
    """Update user statistics"""
    try:
        stats = load_user_stats()
        user_stats = stats.get(user_id, {
            "commands_used": 0,
            "lyrics_searched": 0,
            "tracks_searched": 0,
            "playlist_size": 0,
            "last_used": None,
            "favorite_command": None,
            "command_counts": {}
        })
        
        user_stats["commands_used"] += 1
        user_stats["last_used"] = datetime.now().isoformat()
        user_stats["command_counts"][command] = user_stats["command_counts"].get(command, 0) + 1
        
        if command == "lyrics":
            user_stats["lyrics_searched"] += 1
        elif command == "track":
            user_stats["tracks_searched"] += 1
        
        # Update favorite command
        if user_stats["command_counts"]:
            user_stats["favorite_command"] = max(
                user_stats["command_counts"], 
                key=user_stats["command_counts"].get
            )
        
        stats[user_id] = user_stats
        await save_user_stats(stats)
    except Exception as e:
        logger.error(f"Error updating user stats: {e}")

# Bot setup
intents = discord.Intents.default()
intents.message_content = False  # We don't need message content for slash commands
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Bot startup event"""
    print("=" * 50)
    print(f"🎵 Bot connected as {bot.user}")
    print("=" * 50)
    
    try:
        # Force clear and sync commands
        GUILD_ID = 1411434543981789304
        guild = discord.Object(id=GUILD_ID)
        
        # Clear existing commands
        bot.tree.clear_commands(guild=guild)
        
        # Sync to guild (immediate)
        synced_guild = await bot.tree.sync(guild=guild)
        print(f"✅ Synced {len(synced_guild)} commands to guild {GUILD_ID}")
        
        # Also try global sync
        synced_global = await bot.tree.sync()
        print(f"✅ Synced {len(synced_global)} commands globally")
        
        # List all registered commands
        print(f"📋 Registered commands: {[cmd.name for cmd in synced_guild]}")
        
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
    
    print("🎵 LyricLounge is fully operational! 🎵")
    print("=" * 50)

async def create_music_api():
    """Create MusicAPI instance"""
    try:
        session = aiohttp.ClientSession()
        return MusicAPI(session, lastfm_key=LASTFM_KEY)
    except Exception as e:
        logger.error(f"Error creating MusicAPI: {e}")
        return None

@bot.event
async def setup_hook():
    """Setup hook for bot initialization"""
    bot.music_api = await create_music_api()
    if not bot.music_api:
        logger.error("Failed to initialize MusicAPI")

# Error handling
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Global error handler for slash commands"""
    logger.error(f"Command error: {error}")
    
    embed = discord.Embed(
        title="❌ Command Error",
        description="An error occurred while processing your command.",
        color=0xF44336
    )
    
    if isinstance(error, app_commands.CommandOnCooldown):
        embed.description = f"Command is on cooldown. Try again in {error.retry_after:.1f} seconds."
    
    try:
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        logger.error(f"Error sending error message: {e}")

# ============== CORE COMMANDS ==============

@bot.tree.command(name="help", description="Show all available commands with examples")
async def help_command(interaction: discord.Interaction):
    """Help command showing all available commands"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "help")
    
    embed = discord.Embed(
        title="🎵 LyricLounge - Complete Command Guide",
        description="**Your ultimate music Discord bot companion!**\n",
        color=0x1DB954
    )
    
    # Core Commands
    embed.add_field(
        name="📝 **Core Commands**",
        value="""
        `/help` - Show this help message
        `/lyrics Song Title - Artist` - Get song lyrics
        `/track Song Title - Artist` - Get detailed track info
        `/search query` - Search for songs by name/artist
        `/stats` - View your usage statistics
        """,
        inline=False
    )
    
    # Discovery Commands
    embed.add_field(
        name="🎯 **Music Discovery**",
        value="""
        `/trending [1-20]` - Show trending tracks
        `/artist_top Artist Name [1-15]` - Get artist's top songs
        `/recommend genre` - Get genre recommendations
        `/mood happy/sad/chill/etc` - Get mood-based songs
        `/artist_info Artist Name` - Get artist information
        `/similar Artist Name` - Find similar artists
        """,
        inline=False
    )
    
    # Playlist Commands
    embed.add_field(
        name="📋 **Playlist Management**",
        value="""
        `/playlist_add Song - Artist` - Add to playlist
        `/playlist_view` - View your playlist
        `/playlist_remove number` - Remove song by position
        `/playlist_clear` - Clear entire playlist
        `/playlist_search query` - Search in your playlist
        `/playlist_shuffle [1-10]` - Show random playlist songs
        """,
        inline=False
    )
    
    embed.add_field(
        name="💡 **Pro Tips**",
        value="• Use exact format: `Song Title - Artist Name`\n• Try `/search` if unsure of exact names\n• Build your playlist with `/playlist_add`\n• Discover new music with `/mood` and `/recommend`",
        inline=False
    )
    
    embed.set_footer(text="🎶 LyricLounge - Where every beat finds its voice!")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="lyrics", description="Get song lyrics")
@app_commands.describe(query="Song format: 'Title - Artist'")
async def lyrics(interaction: discord.Interaction, query: str):
    """Get lyrics for a song"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "lyrics")
    
    if not bot.music_api:
        await interaction.followup.send("❌ Music API not available. Please try again later.")
        return
    
    # Parse query
    if " - " not in query:
        embed = discord.Embed(
            title="❌ Invalid Format",
            description="Please use format: `/lyrics Song Title - Artist Name`\n\n**Examples:**\n• `/lyrics Shape of You - Ed Sheeran`\n• `/lyrics Bohemian Rhapsody - Queen`",
            color=0xF44336
        )
        await interaction.followup.send(embed=embed)
        return
    
    title, artist = query.split(" - ", 1)
    title, artist = title.strip(), artist.strip()
    
    try:
        result = await bot.music_api.get_lyrics(title, artist)
        
        if not result:
            embed = discord.Embed(
                title="🔍 No Lyrics Found",
                description=f"No lyrics found for **{title}** by **{artist}**",
                color=0xFF9800
            )
            embed.add_field(name="💡 Try:", value="• Check spelling\n• Use `/search` to find exact song name\n• Try without special characters", inline=False)
            await interaction.followup.send(embed=embed)
            return
        
        # Extract lyrics text
        lyrics_text = result.get("plain_lyrics") or result.get("synced_lyrics", "")
        song_title = result.get("title", title)
        song_artist = result.get("artist", artist)
        
        if not lyrics_text:
            await interaction.followup.send(f"❌ No lyrics content available for **{song_title}** by **{song_artist}**")
            return
        
        # Create embed with lyrics
        embed = discord.Embed(
            title=f"🎵 {song_title}",
            description=f"**Artist:** {song_artist}",
            color=0x1DB954
        )
        
        if result.get("album"):
            embed.add_field(name="💿 Album", value=result["album"], inline=True)
        
        if result.get("source"):
            embed.add_field(name="📡 Source", value=result["source"], inline=True)
        
        # Split lyrics if too long
        max_length = 1900
        if len(lyrics_text) <= max_length:
            embed.add_field(name="📜 Lyrics", value=f"``````", inline=False)
            await interaction.followup.send(embed=embed)
        else:
            # Send first part with embed
            first_chunk = lyrics_text[:max_length]
            embed.add_field(name="📜 Lyrics (Part 1)", value=f"``````", inline=False)
            await interaction.followup.send(embed=embed)
            
            # Send remaining parts
            remaining = lyrics_text[max_length:]
            chunks = [remaining[i:i+max_length] for i in range(0, len(remaining), max_length)]
            
            for i, chunk in enumerate(chunks, 2):
                await interaction.followup.send(f"``````")
        
    except Exception as e:
        logger.error(f"Lyrics error: {e}")
        await interaction.followup.send(f"❌ Error fetching lyrics: {str(e)[:100]}...")

@bot.tree.command(name="track", description="Get detailed track information")
@app_commands.describe(query="Song format: 'Title - Artist'")
async def track(interaction: discord.Interaction, query: str):
    """Get track metadata"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "track")
    
    if not bot.music_api:
        await interaction.followup.send("❌ Music API not available. Please try again later.")
        return
    
    # Parse query
    if " - " not in query:
        embed = discord.Embed(
            title="❌ Invalid Format",
            description="Please use format: `/track Song Title - Artist Name`",
            color=0xF44336
        )
        await interaction.followup.send(embed=embed)
        return
    
    title, artist = query.split(" - ", 1)
    title, artist = title.strip(), artist.strip()
    
    try:
        info = await bot.music_api.get_track_info(title, artist)
        
        if not info:
            embed = discord.Embed(
                title="🔍 Track Not Found",
                description=f"No information found for **{title}** by **{artist}**",
                color=0xFF9800
            )
            embed.add_field(name="💡 Try:", value="• Check spelling\n• Use `/search` to find exact song name", inline=False)
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"🎵 {info.get('title', title)}",
            color=0x1DB954
        )
        
        # Artists
        if info.get("artists"):
            artist_names = [a.get("name", "Unknown") for a in info["artists"]]
            embed.add_field(name="🎤 Artist(s)", value=", ".join(artist_names), inline=False)
        
        # Duration
        if info.get("duration_formatted"):
            embed.add_field(name="⏱️ Duration", value=info["duration_formatted"], inline=True)
        
        # Album and release info
        if info.get("releases") and info["releases"]:
            release = info["releases"][0]
            if release.get("title"):
                embed.add_field(name="💿 Album", value=release["title"], inline=True)
            if release.get("date"):
                embed.add_field(name="📅 Release", value=release["date"], inline=True)
        
        # Country
        if info.get("country"):
            embed.add_field(name="🌍 Country", value=info["country"], inline=True)
        
        # Tags/Genres
        if info.get("tags"):
            tags = ", ".join(info["tags"][:5])
            embed.add_field(name="🏷️ Tags", value=tags, inline=False)
        
        # Footer with confidence score
        footer_text = "Source: MusicBrainz"
        if info.get("score"):
            footer_text += f" • Match: {info['score']}%"
        embed.set_footer(text=footer_text)
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Track info error: {e}")
        await interaction.followup.send(f"❌ Error fetching track info: {str(e)[:100]}...")

@bot.tree.command(name="search", description="Search for songs by partial name")
@app_commands.describe(query="Search term (song, artist, or keywords)")
async def search_songs(interaction: discord.Interaction, query: str):
    """Search for songs"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "search")
    
    if len(query.strip()) < 2:
        embed = discord.Embed(
            title="❌ Search Too Short",
            description="Please provide at least 2 characters.",
            color=0xF44336
        )
        await interaction.followup.send(embed=embed)
        return
    
    try:
        url = "https://api.deezer.com/search"
        params = {"q": query, "limit": 10}
        
        if not bot.music_api or not bot.music_api.session:
            await interaction.followup.send("❌ Search service unavailable.")
            return
        
        async with bot.music_api.session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Search service temporarily unavailable.")
                return
            
            data = await resp.json()
            if not data.get("data"):
                embed = discord.Embed(
                    title="🔍 No Results",
                    description=f"No results found for: **{query}**",
                    color=0xFF9800
                )
                embed.add_field(name="💡 Try:", value="• Different keywords\n• Check spelling\n• Try artist name only", inline=False)
                await interaction.followup.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"🔍 Search Results: '{query}'",
                color=0x00BCD4
            )
            
            results = []
            for i, track in enumerate(data["data"][:10], 1):
                title = track.get("title", "Unknown")
                artist = track.get("artist", {}).get("name", "Unknown")
                duration = track.get("duration", 0)
                
                # Format duration
                if duration:
                    mins, secs = divmod(duration, 60)
                    duration_str = f" ({mins}:{secs:02d})"
                else:
                    duration_str = ""
                
                results.append(f"**{i}.** {title} - {artist}{duration_str}")
            
            embed.description = "\n".join(results)
            embed.set_footer(text="💡 Use /lyrics or /track with 'Song - Artist' format")
            
            await interaction.followup.send(embed=embed)
            
    except Exception as e:
        logger.error(f"Search error: {e}")
        await interaction.followup.send(f"❌ Search error: {str(e)[:100]}...")

@bot.tree.command(name="stats", description="View your music discovery statistics")
async def user_stats(interaction: discord.Interaction):
    """Show user statistics"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "stats")
    
    user_id = str(interaction.user.id)
    stats = load_user_stats()
    user_stats = stats.get(user_id, {})
    
    if not user_stats or user_stats.get("commands_used", 0) <= 1:
        embed = discord.Embed(
            title="📊 Your Music Stats",
            description="Start using LyricLounge commands to build your stats!",
            color=0x607D8B
        )
        await interaction.followup.send(embed=embed)
        return
    
    embed = discord.Embed(
        title=f"📊 Music Stats for {interaction.user.display_name}",
        color=0x2196F3
    )
    
    # Basic stats
    embed.add_field(name="🎵 Commands Used", value=f"{user_stats.get('commands_used', 0)}", inline=True)
    embed.add_field(name="📝 Lyrics Searched", value=f"{user_stats.get('lyrics_searched', 0)}", inline=True)
    embed.add_field(name="🎵 Tracks Searched", value=f"{user_stats.get('tracks_searched', 0)}", inline=True)
    
    # Playlist stats
    playlists = load_playlists()
    playlist_size = len(playlists.get(user_id, []))
    embed.add_field(name="📋 Playlist Size", value=f"{playlist_size} songs", inline=True)
    
    # Favorite command
    if user_stats.get("favorite_command"):
        embed.add_field(name="⭐ Favorite Command", value=f"`/{user_stats['favorite_command']}`", inline=True)
    
    # Last activity
    if user_stats.get("last_used"):
        try:
            last_used = datetime.fromisoformat(user_stats["last_used"])
            embed.add_field(name="🕐 Last Active", value=last_used.strftime("%Y-%m-%d %H:%M"), inline=True)
        except:
            pass
    
    embed.set_footer(text="Keep exploring music with LyricLounge! 🎶")
    await interaction.followup.send(embed=embed)

# ============== DISCOVERY COMMANDS ==============

@bot.tree.command(name="trending", description="Get trending music tracks")
@app_commands.describe(limit="Number of tracks to show (1-20)")
async def trending(interaction: discord.Interaction, limit: int = 10):
    """Show trending tracks"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "trending")
    
    if limit < 1 or limit > 20:
        await interaction.followup.send("❌ Limit must be between 1 and 20.")
        return
    
    try:
        if not bot.music_api:
            await interaction.followup.send("❌ Music service unavailable.")
            return
        
        tracks = await bot.music_api.get_trending_tracks(limit)
        
        if not tracks:
            await interaction.followup.send("❌ No trending tracks available right now.")
            return
        
        embed = discord.Embed(
            title="🔥 Trending Tracks",
            color=0xFF1744
        )
        
        track_list = []
        for i, track in enumerate(tracks[:limit], 1):
            track_list.append(f"**{i}.** {track['title']} - {track['artist']}")
        
        embed.description = "\n".join(track_list)
        embed.set_footer(text="Source: Deezer Charts • Updated daily")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Trending error: {e}")
        await interaction.followup.send(f"❌ Error fetching trending tracks: {str(e)[:100]}...")

@bot.tree.command(name="artist_top", description="Get an artist's top tracks")
@app_commands.describe(artist="Artist name", limit="Number of tracks (1-15)")
async def artist_top(interaction: discord.Interaction, artist: str, limit: int = 10):
    """Get artist's top tracks"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "artist_top")
    
    if limit < 1 or limit > 15:
        await interaction.followup.send("❌ Limit must be between 1 and 15.")
        return
    
    try:
        if not bot.music_api:
            await interaction.followup.send("❌ Music service unavailable.")
            return
        
        tracks = await bot.music_api.search_artist_top_tracks(artist, limit)
        
        if not tracks:
            embed = discord.Embed(
                title="🔍 Artist Not Found",
                description=f"No tracks found for: **{artist}**",
                color=0xFF9800
            )
            embed.add_field(name="💡 Try:", value="• Check spelling\n• Try different artist name", inline=False)
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"🎤 Top Tracks - {artist}",
            color=0x9C27B0
        )
        
        track_list = []
        for i, track in enumerate(tracks[:limit], 1):
            track_info = f"**{i}.** {track['title']}"
            if track.get('album') and track['album'] != 'Unknown':
                track_info += f"\n     *Album: {track['album']}*"
            track_list.append(track_info)
        
        embed.description = "\n".join(track_list)
        embed.set_footer(text="Source: Deezer • Based on popularity")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Artist top error: {e}")
        await interaction.followup.send(f"❌ Error fetching artist tracks: {str(e)[:100]}...")

@bot.tree.command(name="recommend", description="Get music recommendations by genre")
@app_commands.describe(genre="Genre (rock, pop, jazz, electronic, classical, etc.)")
async def recommend(interaction: discord.Interaction, genre: str):
    """Get genre-based recommendations"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "recommend")
    
    try:
        url = "https://api.deezer.com/search"
        params = {"q": f"genre:{genre}", "limit": 10}
        
        if not bot.music_api or not bot.music_api.session:
            await interaction.followup.send("❌ Music service unavailable.")
            return
        
        async with bot.music_api.session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Recommendation service unavailable.")
                return
            
            data = await resp.json()
            if not data.get("data"):
                embed = discord.Embed(
                    title="🔍 Genre Not Found",
                    description=f"No recommendations for: **{genre}**",
                    color=0xFF9800
                )
                embed.add_field(name="💡 Popular Genres:", value="rock, pop, jazz, electronic, classical, hip-hop, country, reggae, blues, folk", inline=False)
                await interaction.followup.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"🎯 {genre.title()} Recommendations",
                color=0xFF5722
            )
            
            recommendations = []
            for i, track in enumerate(data["data"][:10], 1):
                title = track.get("title", "Unknown")
                artist = track.get("artist", {}).get("name", "Unknown")
                recommendations.append(f"**{i}.** {title} - {artist}")
            
            embed.description = "\n".join(recommendations)
            embed.set_footer(text=f"Genre: {genre.title()} • Source: Deezer")
            
            await interaction.followup.send(embed=embed)
            
    except Exception as e:
        logger.error(f"Recommend error: {e}")
        await interaction.followup.send(f"❌ Error fetching recommendations: {str(e)[:100]}...")

@bot.tree.command(name="mood", description="Get songs based on your current mood")
@app_commands.describe(mood="Your mood (happy, sad, energetic, chill, romantic, angry, etc.)")
async def mood(interaction: discord.Interaction, mood: str):
    """Get mood-based songs"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "mood")
    
    # Mood to search term mapping
    mood_keywords = {
        "happy": "upbeat pop dance cheerful",
        "sad": "melancholy emotional ballad",
        "energetic": "high energy rock electronic",
        "chill": "ambient relaxing indie acoustic",
        "romantic": "love romantic ballad",
        "angry": "aggressive metal rock",
        "nostalgic": "classic oldies retro",
        "focused": "instrumental ambient",
        "party": "dance club upbeat",
        "workout": "gym motivation energy"
    }
    
    search_term = mood_keywords.get(mood.lower(), f"{mood} music")
    
    try:
        url = "https://api.deezer.com/search"
        params = {"q": search_term, "limit": 8}
        
        if not bot.music_api or not bot.music_api.session:
            await interaction.followup.send("❌ Music service unavailable.")
            return
        
        async with bot.music_api.session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Mood service unavailable.")
                return
            
            data = await resp.json()
            if not data.get("data"):
                embed = discord.Embed(
                    title="🔍 Mood Not Found",
                    description=f"No songs found for mood: **{mood}**",
                    color=0xFF9800
                )
                embed.add_field(name="💡 Available Moods:", value="happy, sad, energetic, chill, romantic, angry, nostalgic, focused, party, workout", inline=False)
                await interaction.followup.send(embed=embed)
                return
            
            # Mood emojis
            mood_emojis = {
                "happy": "😊", "sad": "😢", "energetic": "⚡", "chill": "😌",
                "romantic": "💕", "angry": "😠", "nostalgic": "🕰️", "focused": "🎯",
                "party": "🎉", "workout": "💪"
            }
            
            emoji = mood_emojis.get(mood.lower(), "🎵")
            
            embed = discord.Embed(
                title=f"{emoji} {mood.title()} Mood Playlist",
                color=0x9C27B0
            )
            
            songs = []
            for i, track in enumerate(data["data"][:8], 1):
                title = track.get("title", "Unknown")
                artist = track.get("artist", {}).get("name", "Unknown")
                songs.append(f"**{i}.** {title} - {artist}")
            
            embed.description = "\n".join(songs)
            embed.set_footer(text=f"Mood: {mood.title()} {emoji} • Curated for your vibe")
            
            await interaction.followup.send(embed=embed)
            
    except Exception as e:
        logger.error(f"Mood error: {e}")
        await interaction.followup.send(f"❌ Error fetching mood songs: {str(e)[:100]}...")

@bot.tree.command(name="artist_info", description="Get detailed artist information")
@app_commands.describe(artist="Artist name")
async def artist_info(interaction: discord.Interaction, artist: str):
    """Get artist information"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "artist_info")
    
    try:
        url = "https://api.deezer.com/search/artist"
        params = {"q": artist, "limit": 1}
        
        if not bot.music_api or not bot.music_api.session:
            await interaction.followup.send("❌ Music service unavailable.")
            return
        
        async with bot.music_api.session.get(url, params=params, timeout=10) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Artist info service unavailable.")
                return
            
            data = await resp.json()
            if not data.get("data"):
                embed = discord.Embed(
                    title="🔍 Artist Not Found",
                    description=f"No information found for: **{artist}**",
                    color=0xFF9800
                )
                await interaction.followup.send(embed=embed)
                return
            
            artist_data = data["data"][0]
            embed = discord.Embed(
                title=f"🎤 {artist_data.get('name', artist)}",
                color=0x673AB7
            )
            
            if artist_data.get("picture_medium"):
                embed.set_thumbnail(url=artist_data["picture_medium"])
            
            # Fan count
            if artist_data.get("nb_fan"):
                embed.add_field(name="👥 Fans", value=f"{artist_data['nb_fan']:,}", inline=True)
            
            # Album count
            if artist_data.get("nb_album"):
                embed.add_field(name="💿 Albums", value=f"{artist_data['nb_album']}", inline=True)
            
            # Deezer link
            if artist_data.get("link"):
                embed.add_field(name="🔗 Listen", value=f"[Deezer Profile]({artist_data['link']})", inline=True)
            
            embed.set_footer(text="Source: Deezer")
            await interaction.followup.send(embed=embed)
            
    except Exception as e:
        logger.error(f"Artist info error: {e}")
        await interaction.followup.send(f"❌ Error fetching artist info: {str(e)[:100]}...")

@bot.tree.command(name="similar", description="Find artists similar to your favorite")
@app_commands.describe(artist="Artist name to find similar artists for")
async def similar_artists(interaction: discord.Interaction, artist: str):
    """Find similar artists"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "similar")
    
    try:
        # First find the artist
        search_url = "https://api.deezer.com/search/artist"
        params = {"q": artist, "limit": 1}
        
        if not bot.music_api or not bot.music_api.session:
            await interaction.followup.send("❌ Music service unavailable.")
            return
        
        async with bot.music_api.session.get(search_url, params=params, timeout=10) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Artist search unavailable.")
                return
            
            data = await resp.json()
            if not data.get("data"):
                embed = discord.Embed(
                    title="🔍 Artist Not Found",
                    description=f"Could not find: **{artist}**",
                    color=0xFF9800
                )
                await interaction.followup.send(embed=embed)
                return
            
            artist_data = data["data"][0]
            artist_id = artist_data.get("id")
            artist_name = artist_data.get("name")
            
            # Get related artists
            related_url = f"https://api.deezer.com/artist/{artist_id}/related"
            async with bot.music_api.session.get(related_url, timeout=10) as related_resp:
                if related_resp.status != 200:
                    await interaction.followup.send("❌ Similar artists service unavailable.")
                    return
                
                related_data = await related_resp.json()
                if not related_data.get("data"):
                    await interaction.followup.send(f"❌ No similar artists found for **{artist_name}**")
                    return
                
                embed = discord.Embed(
                    title=f"🎵 Artists Similar to {artist_name}",
                    color=0x4CAF50
                )
                
                similar_list = []
                for i, similar_artist in enumerate(related_data["data"][:8], 1):
                    name = similar_artist.get("name", "Unknown")
                    fans = similar_artist.get("nb_fan", 0)
                    entry = f"**{i}.** {name}"
                    if fans:
                        entry += f" ({fans:,} fans)"
                    similar_list.append(entry)
                
                embed.description = "\n".join(similar_list)
                embed.set_footer(text="Source: Deezer • Based on listening patterns")
                
                await interaction.followup.send(embed=embed)
                
    except Exception as e:
        logger.error(f"Similar artists error: {e}")
        await interaction.followup.send(f"❌ Error finding similar artists: {str(e)[:100]}...")

# ============== PLAYLIST COMMANDS ==============

@bot.tree.command(name="playlist_add", description="Add a song to your personal playlist")
@app_commands.describe(query="Song format: 'Title - Artist'")
async def playlist_add(interaction: discord.Interaction, query: str):
    """Add song to playlist"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "playlist_add")
    
    user_id = str(interaction.user.id)
    playlists = load_playlists()
    
    # Check for duplicates
    user_playlist = playlists.get(user_id, [])
    if query in user_playlist:
        embed = discord.Embed(
            title="⚠️ Already in Playlist",
            description=f"**{query}** is already in your playlist!",
            color=0xFF9800
        )
        await interaction.followup.send(embed=embed)
        return
    
    # Add to playlist
    playlists.setdefault(user_id, []).append(query)
    await save_playlists(playlists)
    
    # Update stats
    stats = load_user_stats()
    user_stats = stats.get(user_id, {})
    user_stats["playlist_size"] = len(playlists[user_id])
    stats[user_id] = user_stats
    await save_user_stats(stats)
    
    embed = discord.Embed(
        title="✅ Added to Playlist",
        description=f"Added **{query}** to your playlist",
        color=0x4CAF50
    )
    embed.add_field(name="📊 Total Songs", value=f"{len(playlists[user_id])} songs", inline=True)
    embed.add_field(name="💡 Tip", value="Use `/playlist_view` to see all songs", inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="playlist_view", description="View your personal playlist")
async def playlist_view(interaction: discord.Interaction):
    """View user playlist"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "playlist_view")
    
    user_id = str(interaction.user.id)
    playlists = load_playlists()
    items = playlists.get(user_id, [])
    
    if not items:
        embed = discord.Embed(
            title="📝 Your Playlist",
            description="Your playlist is empty! 🎵",
            color=0x607D8B
        )
        embed.add_field(name="💡 Getting Started:", value="• `/playlist_add Shape of You - Ed Sheeran`\n• `/search <song>` to find songs first", inline=False)
        await interaction.followup.send(embed=embed)
        return
    
    embed = discord.Embed(
        title=f"📝 {interaction.user.display_name}'s Playlist ({len(items)} songs)",
        color=0x2196F3
    )
    
    # Show songs with numbers
    song_list = []
    for i, song in enumerate(items[:15], 1):  # Show first 15
        song_list.append(f"**{i}.** {song}")
    
    embed.description = "\n".join(song_list)
    
    if len(items) > 15:
        embed.set_footer(text=f"Showing first 15 of {len(items)} songs • Use /playlist_search to find specific songs")
    else:
        embed.set_footer(text="Use /playlist_remove <number> to remove songs")
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="playlist_remove", description="Remove a song from your playlist")
@app_commands.describe(number="Song number to remove (see /playlist_view for numbers)")
async def playlist_remove(interaction: discord.Interaction, number: int):
    """Remove song from playlist"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "playlist_remove")
    
    user_id = str(interaction.user.id)
    playlists = load_playlists()
    
    if user_id not in playlists or not playlists[user_id]:
        embed = discord.Embed(
            title="📝 Empty Playlist",
            description="Your playlist is empty! Nothing to remove.",
            color=0x607D8B
        )
        await interaction.followup.send(embed=embed)
        return
    
    if number < 1 or number > len(playlists[user_id]):
        embed = discord.Embed(
            title="❌ Invalid Number",
            description=f"Please choose between 1 and {len(playlists[user_id])}",
            color=0xF44336
        )
        embed.add_field(name="💡 Tip:", value="Use `/playlist_view` to see song numbers", inline=False)
        await interaction.followup.send(embed=embed)
        return
    
    removed_song = playlists[user_id].pop(number - 1)
    await save_playlists(playlists)
    
    # Update stats
    stats = load_user_stats()
    user_stats = stats.get(user_id, {})
    user_stats["playlist_size"] = len(playlists[user_id])
    stats[user_id] = user_stats
    await save_user_stats(stats)
    
    embed = discord.Embed(
        title="🗑️ Song Removed",
        description=f"Removed **{removed_song}**",
        color=0xF44336
    )
    embed.add_field(name="📊 Remaining", value=f"{len(playlists[user_id])} songs", inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="playlist_clear", description="Clear your entire playlist")
async def playlist_clear(interaction: discord.Interaction):
    """Clear user playlist"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "playlist_clear")
    
    user_id = str(interaction.user.id)
    playlists = load_playlists()
    
    if user_id not in playlists or not playlists[user_id]:
        embed = discord.Embed(
            title="📝 Already Empty",
            description="Your playlist is already empty!",
            color=0x607D8B
        )
        await interaction.followup.send(embed=embed)
        return
    
    song_count = len(playlists[user_id])
    playlists[user_id] = []
    await save_playlists(playlists)
    
    # Update stats
    stats = load_user_stats()
    user_stats = stats.get(user_id, {})
    user_stats["playlist_size"] = 0
    stats[user_id] = user_stats
    await save_user_stats(stats)
    
    embed = discord.Embed(
        title="🗑️ Playlist Cleared",
        description=f"Removed all {song_count} songs from your playlist",
        color=0xF44336
    )
    embed.add_field(name="🎵 Fresh Start", value="Ready to build a new playlist!", inline=False)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="playlist_search", description="Search within your playlist")
@app_commands.describe(query="Search term to find in your playlist")
async def playlist_search(interaction: discord.Interaction, query: str):
    """Search within playlist"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "playlist_search")
    
    user_id = str(interaction.user.id)
    playlists = load_playlists()
    items = playlists.get(user_id, [])
    
    if not items:
        embed = discord.Embed(
            title="📝 Empty Playlist",
            description="Your playlist is empty! Add some songs first.",
            color=0x607D8B
        )
        await interaction.followup.send(embed=embed)
        return
    
    # Search for matches
    query_lower = query.lower()
    matches = [(i+1, song) for i, song in enumerate(items) if query_lower in song.lower()]
    
    if not matches:
        embed = discord.Embed(
            title="🔍 No Matches",
            description=f"No songs match: **{query}**",
            color=0xFF9800
        )
        embed.add_field(name="💡 Try:", value="Different keywords or check spelling", inline=False)
        await interaction.followup.send(embed=embed)
        return
    
    embed = discord.Embed(
        title=f"🔍 Playlist Search: '{query}'",
        description=f"Found {len(matches)} matches:",
        color=0x00BCD4
    )
    
    match_list = []
    for position, song in matches[:10]:  # Show max 10
        match_list.append(f"**{position}.** {song}")
    
    embed.add_field(name="Matches", value="\n".join(match_list), inline=False)
    
    if len(matches) > 10:
        embed.set_footer(text=f"Showing first 10 of {len(matches)} matches")
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="playlist_shuffle", description="Show random songs from your playlist")
@app_commands.describe(count="Number of random songs (1-10)")
async def playlist_shuffle(interaction: discord.Interaction, count: int = 5):
    """Shuffle playlist songs"""
    await interaction.response.defer()
    await update_user_stats(str(interaction.user.id), "playlist_shuffle")
    
    user_id = str(interaction.user.id)
    playlists = load_playlists()
    items = playlists.get(user_id, [])
    
    if not items:
        embed = discord.Embed(
            title="📝 Empty Playlist",
            description="Your playlist is empty! Add some songs first.",
            color=0x607D8B
        )
        await interaction.followup.send(embed=embed)
        return
    
    if count < 1 or count > 10:
        count = 5
    
    # Get random songs
    shuffled = random.sample(items, min(count, len(items)))
    
    embed = discord.Embed(
        title="🔀 Random Songs from Your Playlist",
        color=0x9C27B0
    )
    
    shuffled_list = []
    for i, song in enumerate(shuffled, 1):
        shuffled_list.append(f"**{i}.** {song}")
    
    embed.description = "\n".join(shuffled_list)
    embed.set_footer(text=f"Showing {len(shuffled)} random songs from {len(items)} total")
    
    await interaction.followup.send(embed=embed)

# ============== CLEANUP & SHUTDOWN ==============

async def close_session():
    """Close aiohttp session"""
    try:
        if getattr(bot, "music_api", None) and getattr(bot.music_api, "session", None):
            await bot.music_api.session.close()
            logger.info("Music API session closed")
    except Exception as e:
        logger.error(f"Error closing session: {e}")

@bot.event
async def on_disconnect():
    """Bot disconnect event"""
    await close_session()

def main():
    """Main function to run the bot"""
    if not DISCORD_TOKEN:
        print("❌ ERROR: DISCORD_BOT_TOKEN not found in .env file!")
        print("Please add your bot token to the .env file:")
        print("DISCORD_BOT_TOKEN=your_token_here")
        return
    
    try:
        print("🎵 Starting LyricLounge...")
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n🎵 LyricLounge shutting down gracefully...")
    except Exception as e:
        print(f"❌ Bot error: {e}")
    finally:
        try:
            asyncio.run(close_session())
        except:
            pass
        print("👋 LyricLounge stopped.")

if __name__ == "__main__":
    main()
