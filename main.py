import discord
from dotenv import load_dotenv
import os
from discord_slash import SlashCommand
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, auto_register=True, auto_delete=True)
load_dotenv('.env')

guild_ids = [799092380095348736]

@client.event
async def on_ready():
  print("Build Succeeded.")

@slash.slash(name="ping", description="Displays the ping.")
async def _ping(ctx):
    await ctx.send(content=f":ping_pong: Pong! ({client.latency*1000}ms)")

@slash.slash(name="echo", description="Echo's text back to you.", options=[manage_commands.create_option("string", "A random string.", SlashCommandOptionType.STRING, True)])
async def _echo(ctx, string):
    await ctx.send(content=string)

@slash.slash(name="announce", description="Makes an announcement.", options=[manage_commands.create_option("channel", "The channel you want to send the announcement to.", SlashCommandOptionType.CHANNEL, True), manage_commands.create_option("message", "your message", SlashCommandOptionType.STRING, True)])
async def _announce(ctx, channel, message):
  if ctx.author.guild_permissions.administrator == True:
    await channel.send(f"{message}")
  else:
    await ctx.send("You aren't an administrator!")

@slash.slash(name="warn", description="Warns a user.", options=[manage_commands.create_option("user", "A member", SlashCommandOptionType.USER, True), manage_commands.create_option("reason", "The reason for the warn.", SlashCommandOptionType.STRING, True)])
async def _warn(ctx, user, reason):
  if ctx.author.guild_permissions.administrator == True:
    embed=discord.Embed(title=f"{user} has been warned.", description=f"Reason: {reason}")
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You aren't an administrator!")

@slash.slash(name="Lock", description="Locks a channel", options=[manage_commands.create_option("channel", "The channel you want to lock.", SlashCommandOptionType.CHANNEL, True), manage_commands.create_option("reason", "the reason for locking the channel", SlashCommandOptionType.STRING, True)])
async def _lock(ctx, channel, reason):
  if ctx.author.guild_permissions.administrator == True:
    await ctx.channel.set_permissions(
    ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title=":warning: Channel has been locked!",description="Moderation action")
    embed.add_field(
    name=(f"{ctx.author} has locked this channel!"),
    value=(f"{reason}"))
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You aren't an administrator!")


@slash.slash(name="unlock", description="unlocks a channel", options=[manage_commands.create_option("channel", "The channel you want to lock.", SlashCommandOptionType.CHANNEL, True), manage_commands.create_option("reason", "the reason for unlocking the channel", SlashCommandOptionType.STRING, True)])
async def _unlock(ctx, channel, reason):
  if ctx.author.guild_permissions.administrator == True:
    await ctx.channel.set_permissions(
    ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title=":white_check_mark: Channel has been unlocked!",description="Moderation action")
    embed.add_field(
    name=(f"{ctx.author} has unlocked this channel!"),
    value=(f"{reason}"))
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You aren't an administrator!")

@slash.slash(name="addrole", description="Gives a user a role,", options=[manage_commands.create_option("user", "the user you want to assign the role to.", SlashCommandOptionType.USER, True), manage_commands.create_option("role", "the role you're giving.", SlashCommandOptionType.ROLE, True)])
async def _addrole(ctx, user, role):
  if ctx.author.guild_permissions.administrator == True:
    await user.add_roles(role)
    embed=discord.Embed(title=":gift: Role given", description=f"{role} has been given to {user}")
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You aren't an administrator!")


@slash.slash(name="removerole", description="Removes a role from a user.", options=[manage_commands.create_option("user", "the user you're removing the role from", SlashCommandOptionType.USER, True), manage_commands.create_option("role", "the role you want to remove.", SlashCommandOptionType.ROLE, True)])
async def _removerole(ctx, user, role):
  if ctx.author.guild_permissions.administrator == True:
    await user.remove_roles(role)
    embed=discord.Embed(title=":white_check_mark: Role removed", description="{role} has been removed from {user}")
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You aren't an administrator!")

@slash.slash(name="mute", description="Mutes someone.", options=[manage_commands.create_option("user", "the user you're muting", SlashCommandOptionType.USER, True)])
async def _mute(ctx, user):
  if ctx.author.guild_permissions.administrator == True:
    embed=discord.Embed(title=":no_entry_sign: Member muted", description=f"{user} has been muted.")
    await user.set_permissions.send_messages == False
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You're not an administrator!")

@slash.slash(name="unmute", description="unmutes someone.", options=[manage_commands.create_option("user", "the user you're unmuting", SlashCommandOptionType.USER, True)])
async def _unmute(ctx, user):
  if ctx.author.guild_permissions.administrator == True:
    embed=discord.Embed(title=":white_check_mark: Member unmuted", description=f"{user} has been unmuted.")
    await user.set_permissions.send_messages == True
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You're not an administrator!")

  


client.run(os.getenv('DISCORD_BOT_SECRET'))