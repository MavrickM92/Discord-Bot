import discord
from discord.ext import commands
import random
import asyncio
import math
import os
from discord.utils import get
import urllib.parse, urllib.request, re

import youtube_dl


# Name: Council's Servant
# Date Initiated: 2020-02-04
# Date Last Modified: 2020-04-12
# Programmer Name: Mavrick McBride (ClamorCattus)
# Language Used: Python (discord.py rewrite)
# Description: A bot for music, welcoming members and role assignment
#based on reactions.


COUNCIL_TOKEN = 'NotShowingHereSorry:)'
client = commands.Bot(command_prefix='.')
client.remove_command('help')

players = {}



@client.event
async def on_ready():
    print('Council Servant initialized')
    s = discord.Game(".help for help")
    await client.change_presence(status=discord.Status.online, activity=s)

@client.event
async def on_member_join(member):
    channel = client.get_channel(656627711485149194)
    print(f'{member} has joined the server!')
    await channel.send(f'@{member}\n>>>Welcome to Order of Ruin!')

@client.event
async def on_member_leave(member):
    channel = client.get_channel(656627711485149194)
    print(f'{member} has left the server!')
    await channel.send(f'{member} has left the server!')

@client.command()
async def shutdown(ctx):
    print('Shutting down...')
    await ctx.send('Shutting down...')
    await ctx.bot.logout()

@client.command()
async def help(ctx):
    await ctx.send("To play music, go into a voice channel and type '.join'. Either do .play <url> and give it a direct youtube url, or .search <args> to search youtube and play the top result.")


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, url: str):
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
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: os.remove('song.mp3')) #Make a queue function, make after=queue function array, move to pos 0 after song finished
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = str(name.rsplit('-', 2)[0])
    await ctx.send(f'Playing: {nname}')
    print('Playing\n')

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

@client.command(aliases=['skip','s'])
async def stop(ctx):
    print('\nSong Skipped!')
    await ctx.send('Song skipped!')
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    

@client.event
async def on_raw_reaction_add(payload):
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
                await member.add_roles(role)
                print('done.')
            else:
                print('member not found')
        else:
            print('role not found')

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

@client.command()
async def purge(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount)
    if amount == 1:
        await ctx.send(f"Deleted {len(deleted)} message.")
    else:
        await ctx.send(f"Deleted {len(deleted)} messages.")

client.run(COUNCIL_TOKEN)