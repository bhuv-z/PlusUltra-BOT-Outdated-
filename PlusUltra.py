import discord
from discord.ext import commands
import asyncio
import os
import traceback
import sys
import datetime

TOKEN = "<<TOKEN ID>>"

Client = discord.Client()
bot = commands.Bot(command_prefix="R!")
ver = '1.0.0'

bot.remove_command('help')  # remove default help command

# -------------------- Loading Cogs(extensions) ------------------------------------#
initial_extensions = ['cogs.commandErrorHandler']
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
# ----------------------------------------------------------------------------------#


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Created by Blaz#7282')

# ------------------GLOBAL VARIABES----------------------------------------#
cmdPrfx = bot.command_prefix
owner = "Blaz#7282"
ownerId = 155418649066840064  # bot owner id goes here

currPath = os.getcwd()
assetsPath = currPath + "\\charAssets\\"
filepath = os.path.join(assetsPath, "charNameList")
charListFile = open(filepath, 'r')
# -------------------------------------------------------------------------#

# ----------------COMMANDS LIST--------------------------------------------#
Rchar = cmdPrfx + "char <charname>"
Rcharlist = cmdPrfx + "charlist"
Rhelp = cmdPrfx + "help"
# -------------------------------------------------------------------------#


# test
@bot.command()
async def test(ctx, *, arg):
    if ctx.message.author.id == ownerId:  # check if owner
        await ctx.send(arg + " <-- that means the bot is online.. nya >.<")


# About Command
@bot.command()
async def about(ctx):
    aboutEmbed = discord.Embed(
        title="A database Bot for Smash Rising" ,
        description="\n__\n__",
        color=0x00ffd8,
        timestamp=datetime.datetime.now()
    )
    aboutEmbed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    aboutEmbed.set_thumbnail(url=bot.user.avatar_url)
    aboutEmbed.add_field(name="Made By", value=owner)
    aboutEmbed.add_field(name="Version", value=ver, inline=False)
    aboutEmbed.add_field(name="Git Repository", value="link\n__\n__")
    aboutEmbed.add_field(name="Contributor(s)", value="**TurboTacho#6590** - Data collection and compilation\n__\n__")

    await ctx.send(embed=aboutEmbed)

# Help command
@bot.command()
async def help(ctx):
    helpEmbed = discord.Embed(
        title="WATASHI GA KITA!!!",
        description="Yo! I'm a database bot for BNHA Smash Rising\n__\n__\n",
        color=0x00ffd8
    )
    helpEmbed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    helpEmbed.add_field(name="Command List", value="\n__\n__\n")
    helpEmbed.add_field(name=Rcharlist, value="Displays a list of characters currently in the "
                                                                    "database, and the ordering of their names\n__\n__\n", inline=False)
    helpEmbed.add_field(name=Rchar, value="Displays the stats of playable characters"
                                                                           "who are currently in the database\n"
                                                                           "**Note:** Use %s to get a list of characters"
                                                                           " and their correct spelling \n__\n__\n" % Rcharlist, inline=False)
    helpEmbed.set_thumbnail(url=bot.user.avatar_url)
    helpEmbed.set_footer(text="Made by " + owner, icon_url=bot.get_user(id=ownerId).avatar_url)
    await ctx.send(embed=helpEmbed)


# charlist
@bot.command()
async def charlist(ctx):
    charListEmbed = discord.Embed(
        title="Character List",
        description=charListFile.read(),
        color=discord.Color.orange()
    )
    charListEmbed.add_field(name="Note:", value="Use the exact spelling and name order you find in this list to use in R!char <charName>")
    await ctx.send(embed=charListEmbed)


# playable char stats BEGIN
@bot.command(pass_context=True)
async def char(ctx, *, arg):
    charName = arg
    charEmbed = discord.Embed(
        title=charName,
        description="test"
    )
    msg = None
    try:
        msg = await  ctx.send(embed=statsEmbed(charName))
    except (FileNotFoundError, discord.errors.HTTPException):
        errorEmbed = discord.Embed(
            title="There is either a typo in the name, or the character you have entered does "
                  "does not exist in the database",
            color=discord.Color.red()
        )
        charEmbed.set_author(name="ERRCODE:150")
        await ctx.send(embed=errorEmbed)

    try:
        await msg.add_reaction(emoji="1⃣")
        await msg.add_reaction(emoji="2⃣")
        await msg.add_reaction(emoji="3⃣")
        await msg.add_reaction(emoji="4⃣")
        await msg.add_reaction(emoji="5⃣")
        await msg.add_reaction(emoji="6⃣")
        await msg.add_reaction(emoji="🇸")
    except AttributeError:
        print("Invalid attribute was passed by: " + ctx.message.author.name)

    def check(reaction, user):

        if reaction.message is not None and msg is not None:
            if user == ctx.message.author and \
                        reaction.message.id == msg.id and \
                        (str(reaction.emoji) == "1⃣" or str(reaction.emoji) == "2⃣"
                         or str(reaction.emoji) == "3⃣" or str(reaction.emoji) == "4⃣"
                         or str(reaction.emoji) == "5⃣" or str(reaction.emoji) == "6⃣"
                         or str(reaction.emoji) == "🇸"):
                return True


    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        if msg is not None:
            await ctx.send("Rip, you slow af %s" % (ctx.message.author.mention))
    else:
        try:
            if str(reaction.emoji) == "1⃣":
                await ctx.send(embed=statsEmbed(charName, 1))
            elif str(reaction.emoji) == "2⃣":
                await ctx.send(embed=statsEmbed(charName, 2))
            elif str(reaction.emoji) == "3⃣":
                await ctx.send(embed=statsEmbed(charName, 3))
            elif str(reaction.emoji) == "4⃣":
                await ctx.send(embed=statsEmbed(charName, 4))
            elif str(reaction.emoji) == "5⃣":
                await ctx.send(embed=statsEmbed(charName, 5))
            elif str(reaction.emoji) == "6⃣":
                await ctx.send(embed=statsEmbed(charName, 6))
            elif str(reaction.emoji) == "🇸":
                await ctx.send("you picked 🇸")
        except discord.errors.HTTPException:
            print("dumb exception from same user" + ctx.author.name)


# -------------------STATS EMBED FOR R!char-------------------------------------#
def statsEmbed(charName, rarity=0):
    charEmbed = None
    charFolderPath = assetsPath + charName
    filepath = os.path.join(charFolderPath, "charData")
    if os.path.exists(filepath):
        charFile = open(filepath, "r")
        charLine = charFile.read().split("\n")
        images = charLine[7].split(";")

        if rarity == 0:
            charIntro = charLine[0].split(";")
            charEmbed = discord.Embed(
                title=charIntro[1].upper(),
                description="\n__\n__",
                color=discord.Color.blue()
            )
            charEmbed.add_field(name=">> " + charIntro[2] + " <<", value="**" + charIntro[3] + "**")
            charEmbed.add_field(name="------", value="\nReact the rarity you would like to view", inline=False)
            charEmbed.set_thumbnail(url=images[1])
            charEmbed.set_footer(text="No. " + charIntro[0])

        elif rarity > 0:
            charTitle = charLine[0].split(";")
            charStats = charLine[rarity].split(";")
            charEmbed = discord.Embed(
                title=charTitle[1].upper(),
                description="\n__\n__",
                color=embedColor(int(float(charStats[0])))
            )
            charEmbed.set_thumbnail(url=images[0])
            charEmbed.set_author(name=charStats[0] + "⭐")
            charEmbed.add_field(name="HP", value=charStats[1])
            charEmbed.add_field(name="SP", value=charStats[2], inline=True)
            charEmbed.add_field(name="ATK", value=charStats[3])
            charEmbed.add_field(name="DEF", value=charStats[4], inline=True)
            charEmbed.add_field(name="HIT", value=charStats[5])
            charEmbed.add_field(name="AVO", value=charStats[6], inline=True)
            charEmbed.add_field(name="LUK", value=charStats[7])
            charEmbed.add_field(name="R-Factor Slots", value=charStats[8])
            charEmbed.add_field(name="No. Badges Required", value=charStats[9])

    return charEmbed


def embedColor(rarity):
    if rarity == 6:
        return 0xea8eff  # lavender
    elif rarity == 5:
        return 0x00d8ff  # blue
    elif rarity == 4:
        return 0xffbf00  # gold
    elif rarity == 3:
        return 0xb5b5b5  # silver
    elif rarity == 2:
        return 0xe57e3d  # bronze
    elif rarity == 1:
        return 0x4e894b  # green

# ------------------------------------------------------------------------------#
# playable char stats END


# -------------------------------SET BOT STATUS-------------------------------------#
@bot.command()
async def setstatus(ctx, *, arg=None):
    if ctx.message.author.id == ownerId:
        gameStatus = arg
        if arg == "terminate":
            await bot.change_presence(activity=None)
        else:
            await bot.change_presence(activity=discord.Game(gameStatus))
# ----------------------------------------------------------------------------------#

bot.run(TOKEN)


