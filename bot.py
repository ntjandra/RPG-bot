from discord.ext import commands
import asyncio
import discord
import requests
import shutil
import os
from dotenv import load_dotenv
from abilities import cast_ability
from data.import_data import *

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
                       "    !info Maria```")
        return
    return

### Info Command ###

@client.command()
async def info(ctx, *argument):
    if ctx.author == client.user:
        return
    # Set Default. You can update this in grader.py
    if not argument:
        await ctx.send (
            "Error: Please specify a Character\n"
        )
    if len(argument) == 1:
        # Create embed
        sheet = discord.Embed(title= argument[0] + " Sheet", description = "Combat Info")

        for field, val in characters[argument[0]].items():
            sheet.add_field(name=field, value=val)

        # sheet.set_thumbnail(ctx.author.avatar_url)
        await ctx.send(embed=sheet)
    return


@client.command()
async def cast(ctx, *argument):
    if ctx.author == client.user:
        return
    # Set Default. You can update this in grader.py
    if not argument:
        await ctx.send ("Error: Supply a character and spell name\n")
        return
    if len(argument) == 2:
        # Cast the Spell
        # TODO: Error handling when Spell is not found.
        message = argument[0] + " casted " + argument[1]
        await ctx.send(message)
        # Results log the results of the spells, if any.
        results = cast_ability(argument[0], argument[1])
        await ctx.send(results)
    return

client.run(os.getenv('DISCORD_TOKEN'))
