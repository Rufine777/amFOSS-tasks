import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from music_api import MusicAPI

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
LASTFM_KEY = os.getenv("LASTFM_API_KEY", "")

PLAYLIST_FILE = "playlists.json"
STATS_FILE = "user_stats.json"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def load_json(file, default=None):
    try:
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    except:
        return default or {}

async def save_json(file, data):
    await asyncio.to_thread(lambda: open(file, "w", encoding="utf-8").write(json.dumps(data, indent=2)))

async def update_stats(user_id, command):
    stats = load_json(STATS_FILE, {})
    s = stats.setdefault(user_id, {"commands_used":0,"lyrics_searched":0,"tracks_searched":0,"command_counts":{}})
    s["commands_used"] += 1
    s["command_counts"][command] = s["command_counts"].get(command,0)+1
    s["last_used"] = datetime.now().isoformat()
    if command == "lyrics": s["lyrics_searched"] += 1
    elif command == "track": s["tracks_searched"] += 1
    s["favorite_command"] = max(s["command_counts"], key=s["command_counts"].get)
    await save_json(STATS_FILE, stats)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.music_api = MusicAPI(discord.ClientSession(), lastfm_key=LASTFM_KEY)
    guild = discord.Object(id=YOUR_GUILD_ID)  # replace with your guild ID
    bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)
    print("Commands synced.")

@bot.tree.command(name="help", description="List all commands")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Core Commands:**\n"
        "/help - Show this message\n"
        "/lyrics <song> - <artist> - Get lyrics\n"
        "/track <song> - <artist> - Get track info\n"
        "/search <query> - Search songs\n"
        "/stats - Show your stats",
        ephemeral=True)
    await update_stats(str(interaction.user.id), "help")

@bot.tree.command(name="lyrics", description="Get song lyrics")
@app_commands.describe(query="Format: Title - Artist")
async def lyrics(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    await update_stats(str(interaction.user.id), "lyrics")
    if " - " not in query:
        return await interaction.followup.send("Format must be: Title - Artist", ephemeral=True)
    title, artist = map(str.strip, query.split(" - ", 1))
    result = await bot.music_api.get_lyrics(title, artist)
    if not result or not (result.get("plain_lyrics") or result.get("synced_lyrics")):
        return await interaction.followup.send(f"No lyrics found for '{title}' by '{artist}'.", ephemeral=True)
    embed = discord.Embed(title=f"{title} - {artist}", color=0x1DB954)
    lyrics_text = result.get("plain_lyrics") or result.get("synced_lyrics")
    embed.add_field(name="Lyrics", value=lyrics_text[:1900]+"..." if len(lyrics_text)>1900 else lyrics_text, inline=False)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="track", description="Get track information")
@app_commands.describe(query="Format: Title - Artist")
async def track(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    await update_stats(str(interaction.user.id), "track")
    if " - " not in query:
        return await interaction.followup.send("Format must be: Title - Artist", ephemeral=True)
    title, artist = map(str.strip, query.split(" - ", 1))
    info = await bot.music_api.get_track_info(title, artist)
    if not info:
        return await interaction.followup.send(f"No track info found for '{title}' by '{artist}'.", ephemeral=True)
    embed = discord.Embed(title=f"{info['title']}", color=0x1DB954)
    artists = ", ".join(a['name'] for a in info.get('artists', [])) or "Unknown"
    embed.add_field(name="Artist(s)", value=artists, inline=False)
    embed.add_field(name="Duration", value=info.get("duration_formatted", "Unknown"), inline=True)
    if info.get("releases"):
        embed.add_field(name="Album", value=info["releases"][0].get("title", "Unknown"), inline=True)
    if info.get("date"):
        embed.add_field(name="Release Date", value=info["date"], inline=True)
    if info.get("tags"):
        embed.add_field(name="Tags", value=", ".join(info["tags"][:5]), inline=False)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="search", description="Search for songs")
@app_commands.describe(query="Song, artist, or keywords")
async def search(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    await update_stats(str(interaction.user.id), "search")
    if len(query.strip())<2:
        return await interaction.followup.send("Please provide at least 2 characters for search.", ephemeral=True)
    results = await bot.music_api.search_songs(query)
    if not results:
        return await interaction.followup.send(f"No results found for '{query}'.", ephemeral=True)
    embed = discord.Embed(title=f"Search results for '{query}'", color=0x00BCD4)
    desc = ""
    for i, r in enumerate(results[:10],1):
        dur = f" ({r['duration']})" if r.get("duration") else ""
        desc += f"**{i}.** {r['title']} - {r['artist']}{dur}\n"
    embed.description = desc
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="stats", description="Show your usage stats")
async def stats(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_json(STATS_FILE, {})
    user_stats = data.get(user_id)
    if not user_stats:
        return await interaction.response.send_message("No stats available. Use the bot commands to build stats.", ephemeral=True)
    embed = discord.Embed(title=f"Stats for {interaction.user.display_name}", color=0x2196F3)
    embed.add_field(name="Commands Used", value=str(user_stats.get("commands_used",0)))
    embed.add_field(name="Lyrics Searched", value=str(user_stats.get("lyrics_searched",0)))
    embed.add_field(name="Tracks Searched", value=str(user_stats.get("tracks_searched",0)))
    embed.add_field(name="Favorite Command", value=f"/{user_stats.get('favorite_command','None')}")
    last = user_stats.get("last_used")
    if last:
        embed.add_field(name="Last Used", value=last)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    await update_stats(user_id, "stats")

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
