import os
import re
import asyncio
import json
import discord
import yt_dlp
from discord.ext import commands

#here we give the bots the "intents". Things on discos backend for privilidges or some shit like that m'mm tbh
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
songque = []


#load config.bison ha ha funny get it??? no? oh... anyways now you can read entries in the BISON
with open("config.json") as file:
        config = json.load(file)
        token = config["token"]

#making an olio for the song so you can match title and url in the same place easily
class Song:
    def __init__(self, songtitle, songurl):
        self.songtitle = songtitle
        self.songurl = songurl

class CurrentlyPlaying:
    def __init__(self, song):
        self.song = song

currentlyplaying = CurrentlyPlaying("")

#initialization
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} and soy is intialized")

#!join the voice channel that the user currently occupies, otherwise humiliation ritual
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Prepare for the experience of a lifetime at {channel}")
    else:
        await ctx.send("Ha, don't try to pull a fast one on me pal. I know all your little tricks... *pssst* you(r(e)) not in a channel")

#!leave just fucking leave and destroy the contents of the queue
@bot.command()
async def leave(ctx):
    if ctx.author.guild_permissions.administrator:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("See ya virgins im outta here~")
            songque.clear()
            currentlyplaying.song = ""
    else:
        await ctx.send("I don't think you have the mental capacity to understand this predicament, so I leave you to it...")

#!play get url from user message, sanitize, add song id to songque, combine part(id) to youtube url and use yt-dlp to extract the most epic youtube link ever
@bot.command()
async def play(ctx, *, url: str):
    #a shame ritual for not inviting bot to a channel. There are many of these litered around...
    if ctx.voice_client is None:
        embed = discord.Embed(title="*hides in the Ogre's outhouse*", description="it feels cozy in here and i don't have to look at you...")
        embed.set_image(url="https://images.squarespace-cdn.com/content/v1/56e0c6ac746fb92b0e77f4d4/1567556573339-40FP9W1U6IBPUU07SWC5/Shrek-2-1920x1080.jpg")
        await ctx.send(embed=embed)
        return

    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)

    if match:
        part = match.group(1)
    else:
        await ctx.send("you did something illegal and YOU will be PUNISHED")
        return

    saneUrl = f"https://www.youtube.com/watch?v={part}"
    ydl_opts = { "format": "bestaudio", "quiet": True, "no_warnings": True, "extract_flat": True, }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(saneUrl, download=False)

    song = Song("", "")

    #this gives out an error for no reason, but it works and slaps the bees knees anyway...
    song.songtitle = info['title']
    song.songurl = info['url']

    songque.append(song)
    print(f"added {song.songtitle} to queue")

    #if bot is already playing epic memes on a channel then skip this, otherwise it starts blasting
    if not ctx.voice_client.is_playing():
        await startQueue(ctx)

async def startQueue(ctx):
    if songque:
        await playQue(ctx)
        embed = discord.Embed(title="Now playing", description=currentlyplaying.song, color=discord.Color.red())
        await ctx.send(embed=embed)

async def playQue(ctx):
    if songque:
        currentlyplaying.song = songque[0].songtitle
        source = discord.FFmpegPCMAudio((songque[0].songurl), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        ctx.voice_client.play(source, bitrate=128, after=lambda e: asyncio.run_coroutine_threadsafe(startQueue(ctx), ctx.bot.loop))
        songque.pop(0)
    else:
        currentlyplaying.song = ""

#disintegrates the currently playing song and then continues on the queue
@bot.command()
async def skip(ctx):
    if ctx.author.guild_permissions.administrator:
        ctx.voice_client.stop()
    else:
        await ctx.send("ha skip on deez baalls :DDDDD")

#check how many songs are in the queue currently
@bot.command()
async def queue(ctx):
    if len(songque) == 0:
        embed = discord.Embed(title="Now playing", description=currentlyplaying.song, color=discord.Color.red())
        embed.set_footer(text=f"Queue empty *womp*")
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title="Currently playing", description=currentlyplaying.song, color=discord.Color.red())
    embed.set_footer(text=f"Next song is {songque[0].songtitle} \nQueue lenght {len(songque)}")
    await ctx.send(embed=embed)

# if you belong to admin you get epic message, else
@bot.command()
async def servaa(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send(f"{ctx.author.display_name} bless your kind heart and have a nice day")
    else:
        await ctx.send(f"{ctx.author.display_name} you are a smelly sock and very ugly and gay")

# if you belong to admin you get epic message, else
@bot.command()
async def poonis(ctx):
    embed = discord.Embed()
    embed.set_image(url="https://i.redd.it/izxiqwmhjvg31.jpg")
    await ctx.send(embed=embed)

@bot.command()
async def you(ctx):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title=f"This is {ctx.author.display_name}", description="what a perfect being")
        embed.set_image(url="https://static.wikia.nocookie.net/joke-battles/images/d/df/Gigachad.png/revision/latest?cb=20230812064835")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"This is literally {ctx.author.display_name}", description="see the pain in its eyes")
        embed.set_image(url="https://pbs.twimg.com/media/FC229gYXsAQyWX5?format=jpg&name=large")
        await ctx.send(embed=embed)

@bot.command()
async def naaduz(ctx):
    await ctx.send("https://cdn.discordapp.com/emojis/707336720227631122.webp")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("you have utterly embarrassed yourself, but hey you could try !help or falling to the ground and crying")

bot.run(token)
