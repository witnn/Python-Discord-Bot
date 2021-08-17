import discord
from discord.ext import commands
from utils import *
import random as rd

_intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True)

Bot = commands.Bot(command_prefix="!w ", intents=_intents)


@Bot.event
async def on_ready():
    print(" ")
    print("Bot active")
    print("Name : {}".format(Bot.user.name))
    print("Access " + str(len(set(Bot.get_all_members()))) + " users!")

    await Bot.change_presence(activity=discord.Game('!w info'), status=discord.Status.online)


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=welcomeChannelName)
    await channel.send(f'**{member} joined the server!**')


@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name=goodbyeChannelName)
    await channel.send(f'**{member} left the server**')


@Bot.event  # Messege delete action
async def on_message_delete(message):
    userControl = message.author != Bot.user
    commandControl = str(message.content)[0:2] != "!w"

    log_channel = discord.utils.get(message.guild.text_channels, name=logChannelName)
    if userControl and commandControl:
        who = str(message.author)
        msgContent = str(message.content)
        channelName = str(message.channel)

        bildirim = f"{who} deleted a message in {channelName} Message content is below\n```{msgContent}```"

        await log_channel.send(bildirim)
        await Bot.process_commands(message)


@Bot.event  # answering back to messages
async def on_message(message):
    if message.author != Bot.user:
        mesaj = str(message.content.lower())
        if mesaj == "hi":
            await message.channel.send("hi")
        elif mesaj == "hello":
            authorName = str(message.author)
            squareIndex = int(authorName.index("#"))

            await message.channel.send(f"hello {authorName[0:squareIndex]} dude")
        elif mesaj[0:8] == "!w speak":
            await message.delete()
        elif mesaj == "stupid bot":
            await message.channel.send("no u")

    await Bot.process_commands(message)


@Bot.command()
async def info(msg):
    await msg.send(infoText)


@Bot.command()
async def speak(ctx, *, arg):
    if str(arg).__contains__("@everyone") == False:
        await ctx.channel.send(arg)
    else:
        await ctx.channel.send("You cannot tag everyone")


@Bot.command()
async def clear(ctx, amount=5):
    if str(ctx.author.roles).lower().__contains__(mod_role):
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f"**{amount} message deleted!**", delete_after=3)
    else:
        await ctx.channel.send("**You are not allowed for use this command.**")


@Bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@Bot.command()
async def roll(ctx):
    await ctx.send(rd.randint(1, 6))


@Bot.command()
async def witcher(ctx):
    await ctx.send(f"{ctx.author}, you are character on witcher : **{rd.choice(characters)}**")


token = Token
Bot.run(token)
