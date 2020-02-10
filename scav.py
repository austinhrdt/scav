""" scav bot """
import os
import asyncio
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='!')  # pylint:disable=invalid-name
client = discord.Client()  # pylint:disable=invalid-name


@bot.event
async def on_ready():
    """ start up ... """
    print(bot.user.name)
    print(bot.user.id)


@bot.command(pass_context=True)
async def scav(ctx, *, content):
    """ scav [user] """
    if is_admin(ctx.message.author):
        if content != "":
            await isolate(ctx, content)
        else:
            await speak("media/scav.mp3", get_voice_channel(ctx, "🎭Main Lobby"))


async def isolate(ctx, name):
    """ isolates scav & target """
    try:
        member = find_member(ctx.message.guild.members, name)
        if member:
            await member.edit(voice_channel="🌆Escape From Tarkov", reason="killa")
            await speak("media/scav.mp3", get_voice_channel(ctx, "🌆Escape From Tarkov"))
    except Exception as err: #pylint:disable=broad-except
        print(err)


async def find_member(members, name):
    """ returns member object of target """
    for member in members:
        if member.name == name:
            return member
    return None


async def speak(filename, voice_channel):
    """ play sound """
    if voice_channel is not None:
        vc = await voice_channel.connect()  # pylint:disable=invalid-name
        vc.play(discord.FFmpegPCMAudio(filename),
                after=lambda e: print('done'))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()


def get_voice_channel(ctx, name):
    """ returns voice channel """
    for channel in ctx.message.guild.voice_channels:
        if channel.name == name:
            return channel
    return None


def is_admin(member):
    """ determines if admin """
    for role in member.roles:
        if role.name in ADMIN_ROLES:
            return True
    return False


ADMIN_ROLES = [
    "adminnss",
    "Shareholder",
    "Trailer Park Supervisor",
    "The OG's"]


bot.run(os.getenv("DISCORD_TOKEN"))
