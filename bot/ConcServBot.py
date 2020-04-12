import discord
from discord.ext import commands
import random
import asyncio
import math
import os
from discord.utils import get
import urllib.parse, urllib.request, re

import youtube_dl
##########################################################################

# Name: Council's Servant
# Date Initiated: 2020-02-04
# Date Last Modified: 2020-04-12
# Programmer Name: Mavrick McBride (ClamorCattus)
# Language Used: Python (discord.py rewrite)
# Description: A bot for music, welcoming members and role assignment
#based on reactions.

# [!] THIS IS NOT FINISHED [!]
# I plan on working more on this. Right now, it is very flawed.
# You must install FFmpeg and make it a Environment Variable for your user, under 'Path'
# 'ffmpeg.exe', 'ffplay.exe', and 'ffprobe.exe', must be placed in the same folder as the Python file
############################################################################


COUNCIL_TOKEN = 'NotShowingHereSorry:)' # Bot's token. Add your own bot's token.
client = commands.Bot(command_prefix='.') # Bot Prefix
client.remove_command('help') # Remove premade command 'help' to implement my own


@client.event
async def on_ready():
    print('Council Servant initialized')
    s = discord.Game(".help for help")
    await client.change_presence(status=discord.Status.online, activity=s)

@client.event
async def on_member_join(member):
    channel = client.get_channel(656627711485149194) # Id of channel I want to send message to
    print(f'{member} has joined the server!')
    await channel.send(f'@{member}\n>>>Welcome to Order of Ruin!')

@client.event
async def on_member_leave(member):
    channel = client.get_channel(656627711485149194)
    print(f'{member} has left the server!')
    await channel.send(f'{member} has left the server!')
    
@client.command()
async def help(ctx): # Help command
    await ctx.send("To play music, go into a voice channel and type '.join'. Either do .play <url> and give it a direct youtube url, or .search <args> to search youtube and play the top result.")


    # Join voice channel you are in
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

    # Leave voice channel
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

    # The command .play only takes in direct URL's, (usage: .play <URL>)
    # The way this works, the computer downloads the song and streams it
@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there: # Checking if the file "song.mp3" is already there
            os.remove("song.mp3")
            print('Removed old song file')
    except PermissionError: # If song is playing, this is outputted
        print('Trying to delete song file, but its being played')
        await ctx.send('ERROR: Music playing')
        return

    await ctx.send('Getting song...')

    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = { # Options for Youtube Downloader
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading song now...\n')
        ydl.download([url]) # Downloads song of the url

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: os.remove('song.mp3')) # Plays song, and removes the song file when done playing
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = str(name.rsplit('-', 2)[0])
    await ctx.send(f'Playing: {nname}')
    print('Playing\n')

    # Search command takes in a search (usage: .search Nyan Cat)
@client.command()
async def search(ctx, *, search):

    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print('Removed old song file')
    except PermissionError:
        print('Trying to delete song file, but its being played')
        await ctx.send('ERROR: Music playing')
        return

    await ctx.send('Getting song...')

    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading song now...\n')
        ydl.download(['http://www.youtube.com/watch?v=' + search_results[0]])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: os.remove('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    

    nname = str(name.rsplit('-', 2)[0])
    await ctx.send(f'Playing: {nname}')
    print('Playing\n')

    # Command to skip the song
@client.command(aliases=['skip','s'])
async def stop(ctx):
    print('\nSong Skipped!')
    await ctx.send('Song skipped!')
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    

    # This is not a command, it is an event
    # How to use: in "if message_id == 680825135443607572", replace the numbers with the message ID that you want
    # people to react to.
    # 
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 680825135443607572:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'r6': # Checking the reaction emoji's name.
            print('Rainbow Six Siege Role')
            role = discord.utils.get(guild.roles, name='Rainbow Six Siege')
        elif payload.emoji.name == 'justc':
            print('C Role')
            role = discord.utils.get(guild.roles, name='C')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('done.')
            else:
                print('member not found')
        else:
            print('role not found')

            # Remove roles if reaction is removed
            # Repalce message ID with message ID of your choice
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 680825135443607572:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'r6':
            print('Rainbow Six Siege Role')
            role = discord.utils.get(guild.roles, name='Rainbow Six Siege')
        elif payload.emoji.name == 'justc':
            print('C Role')
            role = discord.utils.get(guild.roles, name='C')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('done')
            else:
                print('member not found')
        else:
            print('role not found')

            # A quick command to mass delete messages
            # Usage: .purge <number>
            
@client.command()
async def purge(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount)
    if amount == 1:
        await ctx.send(f"Deleted {len(deleted)} message.") # For grammar
    else:
        await ctx.send(f"Deleted {len(deleted)} messages.") # For grammar

client.run(COUNCIL_TOKEN)
