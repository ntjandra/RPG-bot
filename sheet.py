"""
Helper Functions for character sheet related data
"""


from grammar import sentence
""" 
List of Categories
A Constant list to match the data with game rules. 
"""
RESOURCES_KEYS = ["level", "health", "alchemy", "devotion"]
COMBAT_KEYS = ["weapon_power", "spell_power", "armor", "spell_resist", "shield"]
MULTIPLIER_KEYS = ["heal_shield_mult", "spell_mult", "weapon_mult", "dmg_resist"]
MAX_PAGES = 5 # Because Pages start at 1, this should be 1 greater than usual.


def sort_pages(embed, field, val):
        """
        Orders Character Sheet by Related Fields
        Page 1: Resources and Basic Stats
        Page 2: Combat and Defensive Stats
        Page 3: Resistance and Damage Multipliers
        Page 4: Everything else (Misc. Character Specifics)
        """
        if field in RESOURCES_KEYS:
            embed[1].add_field(name=sentence(field), value=val)
        elif field in COMBAT_KEYS:
            embed[2].add_field(name=sentence(field), value=val)
        elif field in MULTIPLIER_KEYS:
            embed[3].add_field(name=sentence(field), value=val)
        else:
            embed[4].add_field(name=sentence(field), value=val)


async def paginate(client, ctx, message, embeds, page=1):
    """
    Paginates a message using the bot to listen for reactions.
    Client (Bot)
    Ctx = Context
    Message = Discord Message to update
    embeds = List of content for each page.
    page = starting page
    """
    emojis = ["◀️", "▶️"]
    for emoji in emojis:
        await message.add_reaction(emoji)
    while not client.is_closed():
        try:
            react, user = await client.wait_for(
                "reaction_add",
                timeout = 60.0,
                check = lambda r, u: r.emoji in emojis and u.id == ctx.author.id and r.message.id == message.id
            )
            if react.emoji == emojis[0] and page > 1:
                page -= 1
            elif react.emoji == emojis[1] and page < len(embeds) - 2:
                page += 1
            await message.edit(embed=embeds[page])
        except TimeoutError as e:
            print(e)
            await message.delete()
            break
