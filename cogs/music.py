import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.loop = False

    @commands.command(name="play")
    async def play(self, ctx, *, query):
        voice = ctx.author.voice
        if not voice:
            await ctx.send("Join a voice channel first!")
            return

        vc = await voice.channel.connect() if not ctx.voice_client else ctx.voice_client

        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'default_search': 'ytsearch',
            'extract_flat': 'in_playlist',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info['url'] if 'url' in info else info['entries'][0]['url']

        vc.stop()
        vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print("Done"))

        await ctx.send(f"Now playing: {query}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("⏭️ Skipped!")

    @commands.command(name="loop")
    async def loop(self, ctx):
        self.loop = not self.loop
        await ctx.send(f"🔁 Loop is now {'enabled' if self.loop else 'disabled'}")

    @commands.command(name="random")
    async def random(self, ctx):
        import random
        tracks = [
            "lofi chill beats",
            "space ambient music",
            "birthday countdown music",
            "cosmic synthwave"
        ]
        choice = random.choice(tracks)
        await self.play(ctx, query=choice)

async def setup(bot):
    await bot.add_cog(Music(bot))
