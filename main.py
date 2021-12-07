import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import check
from discord_together import DiscordTogether
from decouple import config

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.messages = True


cross = "<:red_cross:917650316512620544>"
tick = "<:green_tick:917650630405926912>"

#kana variables
token = config("TOKEN")
kana_id = 857835279259664403
client = commands.Bot(command_prefix=commands.when_mentioned_or(','), case_insensitive=True, intents=intents)
client.remove_command("help")

DT_OPTIONS = {
    "yt" : "youtube",
    "dc" : "doodle-crew",
    "pr" : "poker",
    "bt" : "betrayal",
    "fh" : "fishing",
    "cs" : "chess",
    "lt" : "letter-tile",
    "ws" : "word-snack",
    "sc" : "spellcast",
    "aw" : "awkword",
    "ck" : "checkers"
}

print(">> DT is awaking...")

def check_event(event):
    for option in list(DT_OPTIONS.keys()):
        if option == event:
            return True
    return False
            
def get_embed(game, user):
    embed = discord.Embed(
        description=f"{tick} Game created ~ `{DT_OPTIONS[game].capitalize()}`\n*Please click on the link to start the game so that others can join you.*",
        color=0xffb0cd
    )
    embed.set_author(
        name=f"Join {user.name} for {DT_OPTIONS[game].capitalize()}!",
        icon_url = user.avatar_url
    )
    return embed

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Discord Together!"))
    client.togetherControl = await DiscordTogether(token)
    print("DT online")

@client.command()
async def games(ctx):
    desc = "> `1. ` ~ `YouTube Together` ~ `yt`\n> `2. ` ~ `Doodle Crew` ~ `dc`\n> `3. ` ~ `Poker` ~ `pr`\n> `4. ` ~ `Betrayal.io` ~ `bt`\n> `5. ` ~ `Fishington.io` ~ `fh`\n> `6. ` ~ `Chess` ~ `cs`\n> `7. ` ~ `Letter Tile` ~ `lt`\n> `8. ` ~ `Word Snack` ~ `ws`\n> `9. ` ~ `Spell Cast` ~ `sc`\n> `10.` ~ `AwkWord` ~ `aw`\n> `11.` ~ `Checkers` ~ `ck`\n"
    emb = discord.Embed(
        description=desc,
        colour=0xffb0cd
    )
    emb.set_author(
        name="Game List",
        icon_url=ctx.author.avatar_url
    )
    emb.set_footer(
        text="Send ,start [prefix for game] to start a game"
    )
    await ctx.send(embed=emb)

@client.command()
async def help(ctx):
    embed = discord.Embed(
        description="Discord Together Bot allows you to access Games which are yet in Beta and play them with your friends!\n*Usage: `,start game_prefix` to start the game.*\n\n*Use `,games` to see the list of games available and their prefixes.*",
        colour=0xffb0cd
    )
    embed.set_author(
        name="Need Help?",
        icon_url=ctx.author.avatar_url
    )
    await ctx.send(embed=embed)

@client.command()
async def start(ctx, *, option=None):
    if ctx.author.voice is None:
        embed = discord.Embed(description=f"{cross} Please join a `Voice channel` to start a game!", colour=0xffb0cd)
        await ctx.send(embed=embed)
    else:
        if option is None:
            embed = discord.Embed(description=f"{cross} Please provide a game prefix to start a game! You can see the available games and their prefixes using `,games` command.", colour=0xffb0cd)
            await ctx.send(embed=embed)
        if option is not None and check_event(option):
            link = await client.togetherControl.create_link(ctx.author.voice.channel.id, f'{DT_OPTIONS[option]}')
            emb = get_embed(option, ctx.author)
            await ctx.send(f"Click on the link to get started!\n{link}", embed=emb)
        elif option is not None and not check_event(option):
            embed = discord.Embed(description=f"{cross} No game found! Please send `,games` to check all the games available.", colour=0xffb0cd)
            await ctx.send(embed = embed)


client.run(token)