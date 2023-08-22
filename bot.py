"""
Main RBG BOT File 
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from abilities import cast_ability
from data.import_data import init_party, save_player, load_player, characters
from grammar import sentence

# Load environment variables
load_dotenv()
client = commands.Bot(command_prefix='!')

# Generate the structure for saves.
if not os.path.exists('saves'):
    os.makedirs('saves')


@client.event
async def on_ready():
    """
    Event To When Bot Is Ready
    """
    print('ready')


client.remove_command('help')


### Command List ###~
@client.command()
async def help(ctx, *argument):
    """
    Help Command
    """
    print('help')
    if not argument:
        await ctx.send("```Commands: \n"
                       "\n !info <characterName> Returns a character stats."
                       "\n !cast <characterName> <spellName> Cast a spell using a character's stats."
                       "\n !help <command>  Displays detailed command info."
                       "\n !save <characterName> <?slot> Save current info to load later."
                       "\n !load <characterName> <?slot> Loads state from file.```")
        return
    if argument[0] == "info" and len(argument) == 1:
        await ctx.send("```Supply a character name and get back it's character sheet."
                       "Defaults combat stats only. \n"
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
    if argument[0] == "save" and len(argument) == 1:
        await ctx.send("```Save a character's sheet. Max 3 save slots. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !save Maria 1```")
    if argument[0] == "load" and len(argument) == 1:
        await ctx.send("```Load a character's sheet updating the values. Defaults to option 1. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !save Maria 1```")
    return


@client.command()
async def info(ctx, *argument):
    """
    Info Command About a Character
    """
    if ctx.author == client.user:
        return
    if not argument:
        await ctx.send(
            "Error: Please specify a Character\n"
        )
    if len(argument) == 1:
        # Create embed
        character = argument[0].lower()
        sheet = discord.Embed(title=sentence(f'{character} Sheet'), description="Combat Info")

        for field, val in characters[character].items():
            sheet.add_field(name=sentence(field), value=val)

        # sheet.set_thumbnail(ctx.author.avatar_url)
        await ctx.send(embed=sheet)
    return


@client.command()
async def cast(ctx, *argument):
    """
    Cast Command
    """
    if ctx.author == client.user:
        return
    if not argument:
        await ctx.send("Error: Supply a character and spell name\n")
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


@client.command()
async def save(ctx, *argument):
    """
    Save Command
    """
    if not argument:
        await ctx.send("Error: Supply a character to save on. \n")
        return
    # Choose a specific character to save data on.
    if len(argument) == 2:
        await ctx.send("Saving... \n")
        character = argument[0].lower()
        message = sentence(save_player(character, argument[1]))
        await ctx.send("Save Complete \n")
        await ctx.send(message)
    return


@client.command()
async def load(ctx, *argument):
    """
    Load Command
    """
    if not argument:
        await ctx.send("Error: Supply a character and number from 1 to 3 \n")
        return
    # Choose a specific character to load data for.
    if len(argument) == 2:
        await ctx.send("Loading... \n")
        character = argument[0].lower()
        message = sentence(load_player(character, argument[1]))
        await ctx.send("Load Complete \n")
        await ctx.send(message)
    return


@client.command()
async def quicksave(ctx, *argument):
    """
    Quicksave Command
    """
    if not argument:
        message = init_party()
        await ctx.send(message)
    return


client.run(os.getenv('DISCORD_TOKEN'))
