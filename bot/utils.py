import re
from PIL import Image
from io import BytesIO
from collections import Counter

from discord.ext.commands.core import NotOwner

import api, discord, logging
from typing import Dict, Any
logger = logging.getLogger(__name__)

def sanitize_filename(filename: str) -> str:
    # Define a regular expression pattern that matches any character not allowed in filenames
    # For Windows, common illegal characters include: / / : * ? " < > |
    # The following pattern keeps only alphanumeric characters, hyphens, underscores, and periods.
    sanitized_filename = re.sub(r'[^A-Za-z0-9._-]', '_', filename)
    return sanitized_filename


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val

    if delta == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    elif max_val == b:
        h = (60 * ((r - g) / delta) + 240) % 360

    s = 0 if max_val == 0 else (delta / max_val)
    v = max_val

    return h, s, v


def get_accent_color(image_bytes, threshold=50):
    image = Image.open(BytesIO(image_bytes))
    image = image.convert('RGB')  # Ensure image RGB

    # Resize image to reduce computation time
    image = image.resize((50, 50))

    # Get pixels as a list of tuples
    pixels = list(image.getdata())

    # Count the frequency of each color
    color_counts = Counter(pixels)

    # Find the dominant color
    dominant_color = color_counts.most_common(1)[0][0]

    # Filter out colors too close to the dominant color
    def color_distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

    accent_color = None
    max_priority = -1

    for color, count in color_counts.items():
        if color_distance(dominant_color, color) > threshold:
            # Convert color to HSV
            _, saturation, brightness = rgb_to_hsv(*color)

            # Calculate priority based on saturation and brightness
            priority = saturation * brightness * count

            if priority > max_priority:
                max_priority = priority
                accent_color = color

    return accent_color


async def update_active_servers(bot: discord.Bot, server_sessions: Dict[Any, Any]):
    active_guilds = []
    for vc in bot.voice_clients:
        if vc.is_playing():
            guild = vc.guild
            session = server_sessions.get(guild.id)
            queue = session.get_queue() if session else []
            song_info = queue.pop(0) # Skip the first item as it's the currently playing song
            history = session.get_history() if session else []
            current_song = {
                "title": song_info['title'],
                "artist": song_info.get('artist'),
                "album": song_info.get('album'),
                "cover": song_info.get('cover'),
                "duration": song_info.get('duration'),
                "playback_start_time": session.playback_start_time,
                "url": song_info['url']
            } if song_info else None
            guild_info = {
                "id": str(guild.id), # Convert to string to avoid overflow in JavaScript
                "name": guild.name,
                "icon": guild.icon.url if guild.icon else None,
                "currentSong": current_song,
                "queue": queue,
                "history": history
            }
            active_guilds.append(guild_info)

    logger.info(f"Updating active servers.")
    await api.update_active_servers(active_guilds)
