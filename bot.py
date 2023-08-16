from discord.ext import commands
import asyncio
import discord
import requests
import shutil
import os
from dotenv import load_dotenv
from abilities import cast_ability
from data.import_data import *
from grammar import sentence

# Load environment variables
load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('ready')

client.remove_command('help')

### Command List ###~
@client.command()
async def help(ctx, *argument):
    print('help')
    if not argument:
        await ctx.send("```Commands: \n"
                       "\n !info <characterName> Returns a character stats."
                       "\n !cast <characterName> <spellName> Cast a spell using a character's stats."
                       "\n !help <command>  Displays detailed command info.```")
        return
    if argument[0] == "info" and len(argument) == 1:
        await ctx.send("```Supply a character name and get back it's character sheet. Defaults combat stats only. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !info Maria```")
        return
    if argument[0] == "cast" and len(argument) == 1:
        await ctx.send("```Cast a spell using a character's stats for scaling and additional effects. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !cast Maria basic```")
        return
    return

### Info Command ###

@client.command()
async def info(ctx, *argument):
    if ctx.author == client.user:
        return
    if not argument:
        await ctx.send (
            "Error: Please specify a Character\n"
        )
    if len(argument) == 1:
        # Create embed
        character = argument[0].lower()
        sheet = discord.Embed(title= sentence(f'{character} Sheet'), description = "Combat Info")

        for field, val in characters[character].items():
            sheet.add_field(name=sentence(field), value=val)

        # sheet.set_thumbnail(ctx.author.avatar_url)
        await ctx.send(embed=sheet)
    return


@client.command()
async def cast(ctx, *argument):
    if ctx.author == client.user:
        return
    if not argument:
        await ctx.send ("Error: Supply a character and spell name\n")
        return
    if len(argument) == 2:
        # Cast the Spell
        # TODO: Error handling when Spell is not found.

        # Reformat to ignore case errors
        character = argument[0].lower()
        skill = argument[1].lower()

        message = sentence(f'{character} casted {skill}')
        await ctx.send(message)

        # Results log the results of the spells, if any.
        results = cast_ability(character, skill)
        await ctx.send(results)
    return

client.run(os.getenv('DISCORD_TOKEN'))
