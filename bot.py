"""
Main RBG BOT File
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from abilities import cast_ability, deal_pain
from data.import_data import init_party, save_player, load_player, characters
from grammar import sentence
from sheet import sort_pages, paginate, MAX_PAGES

# Load environment variables
load_dotenv()


"""
Define Client (Bot) Parameters
Intents are permissions the bot should have. Err on the side of less.
Client is used to define the bot and configure it's event listeners.
Tree stores the commands to send over to the Discord shortcut.
Notes: Use mentions, /, and ! as the prefixes. Intents are now required in the latest version.
"""
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)
# Generate the structure for saves.
if not os.path.exists('saves'):
    os.makedirs('saves')


@client.event
async def on_ready():
    """
    Returns when the bot is ready to accept inputs.
    """
    print("ready")

client.remove_command('help')


@client.hybrid_command(description="Queue up Discord slash commands sync. Make take up to an hour.")
async def sync(ctx):
    """
    Queue up Discord slash commands sync. Make take up to an hour.
    Optional: Fill in Sync with your server. guild=discord.Object(id={os.getenv('DISCORD_TOKEN')})
    """
    synced = await client.tree.sync()
    log = f'{str(len(synced))} Commands Synced'
    print(log)
    await ctx.send(log)
    return


@client.hybrid_command(name='help', description="Lists help info for commands.")
async def help(ctx, bot_command: str = None):
    """
    Help Command
    """
    print('help')
    if ctx.author == client.user:
        return
    if not bot_command:
        await ctx.send(content="```Commands: \n"
                       "\n !info <characterName> <?page> Returns a character stats. Supports pagination."
                       "\n !cast <characterName> <spellName> Cast a spell using a character's stats."
                       "\n !pain <characterName> <damage> <damageType> Calculate damage taken."
                       "\n !help <command>  Displays detailed command info."
                       "\n !save <characterName> <?slot> Save current info to load later."
                       "\n !load <characterName> <?slot> Loads state from file.```")
        return
    if bot_command == "info":
        await ctx.send(content="```Supply a character name and get back it's character sheet."
                       "Defaults combat stats only. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !info Maria```")
        return
    if bot_command == "cast":
        await ctx.send("```Cast a spell using a character's stats for scaling and additional effects. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !cast Maria basic```")
        return
    if bot_command == "pain":
        await ctx.send("```Calculate damage taken by a character. Requires character, damage number, and damage type. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !pain Maria 200 magic```")
        return
    if bot_command == "save":
        await ctx.send("```Save a character's sheet. Max 3 save slots. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !save Maria 1```")
    if bot_command == "load":
        await ctx.send("```Load a character's sheet updating the values. Defaults to option 1. \n"
                       "Usage: \n"
                       "    Lookup Characters: \n"
                       "    !load Maria 1```")
    return


@client.hybrid_command(description="Fetches the character's sheet and displays it in an embed message.")
async def info(ctx, character: str, page: int = 1):
    """
    Command for Character info
    """

    if ctx.author == client.user:
        return
    if not character:
        await ctx.send("Error: Please specify a Character\n")
    else:
        # Create list of embeds
        character = character.lower()
        sheet = [None for _ in range(0, MAX_PAGES+1)]
        for page_no in range(1, MAX_PAGES):
            sheet[page_no] = discord.Embed(title=sentence(f'{character}'), description="Character Info")
            sheet[page_no].set_footer(text=f'Page {page_no}')
            # sheet.set_thumbnail(ctx.author.avatar_url)
        for field, val in characters[character].items():
            # Sort through pages
            sort_pages(sheet, field, val)
            
        message = await ctx.send(embed=sheet[page])
        # Update the message based on content and page.
        await paginate(client, ctx, message, sheet, page)
    return


@client.hybrid_command(description="Casts a skill using a character's stats for calculating raw damage.")
async def cast(ctx, character, skill):
    """
    Cast Command
    """
    if ctx.author == client.user:
        return
    if not character or not skill:
        await ctx.send("Error: Supply a character and spell name\n")
        return
    else:
        # Cast the Spell
        # TODO: Error handling when Spell is not found.

        # Reformat to ignore case errors
        character = character.lower()
        skill = skill.lower()

        message = sentence(f'{character} casted {skill}')
        await ctx.send(message)

        # Results log the results of the spells, if any.
        results = cast_ability(character, skill)
        await ctx.send(results)
    return


@client.hybrid_command(description="Calculates damage taken for a character based on their resistances.")
async def pain(ctx, character=None, dmg=None, dmg_type=None):
    """
    Pain Command
    """
    if ctx.author == client.user:
        return
    if not (character and dmg and dmg_type):
        await ctx.send("Error: Supply a character, damage number, and damage type \n")
        return
    else:
        # Reformat to ignore case errors
        character = character.lower()
        dmg = dmg.lower()
        dmg_type = dmg_type.lower()
        # Results log the results of the damage taken.
        results = deal_pain(character, int(dmg), dmg_type)
        await ctx.send(results)
    return


@client.hybrid_command()
async def save(ctx, character, slot=1):
    """
    Save Command
    """
    if ctx.author == client.user:
        return
    if not character:
        await ctx.send("Error: Supply a character to save on. \n")
        return
    # Choose a specific character to save data on.
    else:
        await ctx.send("Saving... \n")
        character = character.lower()
        message = sentence(save_player(character, slot))
        await ctx.send("Save Complete \n")
        await ctx.send(message)
    return


@client.hybrid_command()
async def load(ctx, character, slot=1):
    """
    Load Command
    """
    if ctx.author == client.user:
        return
    if not character:
        await ctx.send("Error: Supply a character slot to load from \n")
        return
    # Choose a specific character to load data for.
    else:
        await ctx.send("Loading... \n")
        character = character.lower()
        message = sentence(load_player(character, slot))
        await ctx.send(message)
    return


@client.hybrid_command()
async def quicksave(ctx):
    """
    Quicksave Command
    """
    if ctx.author == client.user:
        return
    message = init_party()
    await ctx.send(message)
    return


client.run(os.getenv('DISCORD_TOKEN'))
