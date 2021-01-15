import discord
from dotenv import load_dotenv
import os
from discord_slash import SlashCommand
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, auto_register=True)
load_dotenv('.env')

guild_ids = [799092380095348736]

@client.event
async def on_ready():
  print("Build Succeeded.")

@slash.slash(name="ping", description="Displays the ping.",guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(content=f":ping_pong: Pong! ({client.latency*1000}ms)")

@slash.slash(name="echo", description="Echo's text back to you.", guild_ids=guild_ids, options=[manage_commands.create_option("string", "A random string.", SlashCommandOptionType.STRING, True)])
async def _echo(ctx, string):
    await ctx.send(content=string)

@slash.slash(name="announce", description="Makes an announcement.", guild_ids=guild_ids, options=[manage_commands.create_option("channel", "The channel you want to send the announcement to.", SlashCommandOptionType.CHANNEL, True), manage_commands.create_option("message", "your message", SlashCommandOptionType.STRING, True)])
async def _announce(ctx, channel, message):
  await channel.send(f"{message}")

@slash.slash(name="warn", description="Warns a user.", guild_ids=guild_ids, options=[manage_commands.create_option("user", "A member", SlashCommandOptionType.USER, True), manage_commands.create_option("reason", "The reason for the warn.", SlashCommandOptionType.STRING, True)])
async def _warn(ctx, user, reason):
  if ctx.author.guild_permissions.administrator == True:
    embed=discord.Embed(title=f"{user} has been warned.", description=f"Reason: {reason}")
    await ctx.send(embeds=[embed])
  else:
    await ctx.send("You aren't an administrator!")

@slash.slash(name="Lock", description="Locks a channel", guild_ids=guild_ids, options=[manage_commands.create_option("channel", "The channel you want to lock.", SlashCommandOptionType.CHANNEL, True), manage_commands.create_option("reason", "the reason for locking the channel", SlashCommandOptionType.STRING, True)])
async def _lock(ctx, channel, reason):
  await ctx.channel.set_permissions(
  ctx.guild.default_role, send_messages=False)
  embed = discord.Embed(title=":warning: Channel has been locked!",description="Moderation action")
  embed.add_field(
  name=(f"{ctx.author} has locked this channel!"),
  value=(f"{reason}"))
  await ctx.send(embeds=[embed])


@slash.slash(name="unlock", description="unlocks a channel", guild_ids=guild_ids, options=[manage_commands.create_option("channel", "The channel you want to lock.", SlashCommandOptionType.CHANNEL, True), manage_commands.create_option("reason", "the reason for unlocking the channel", SlashCommandOptionType.STRING, True)])
async def _unlock(ctx, channel, reason):
  await ctx.channel.set_permissions(
  ctx.guild.default_role, send_messages=True)
  embed = discord.Embed(title=":white_check_mark: Channel has been unlocked!",description="Moderation action")
  embed.add_field(
  name=(f"{ctx.author} has unlocked this channel!"),
  value=(f"{reason}"))
  await ctx.send(embeds=[embed])

@slash.slash(name="addrole", description="Gives a user a role,", guild_ids=guild_ids, options=[manage_commands.create_option("user", "the user you want to assign the role to.", SlashCommandOptionType.USER, True), manage_commands.create_option("role", "the role you're giving.", SlashCommandOptionType.ROLE, True)])
async def _addrole(ctx, user, role):
  await user.add_roles(role)
  embed=discord.Embed(title=":gift: Role given", description=f"{role} has been given to {user}")
  await ctx.send(embeds=[embed])


@slash.slash(name="removerole", description="Removes a role from a user.", guild_ids=guild_ids, options=[manage_commands.create_option("user", "the user you're removing the role from", SlashCommandOptionType.USER, True), manage_commands.create_option("role", "the role you want to remove.", SlashCommandOptionType.ROLE, True)])
async def _removerole(ctx, user, role):
  await user.remove_roles(role)
  embed=discord.Embed(title=":white_check_mark: Role removed", description="{role} has been removed from {user}")
  await ctx.send(embeds=[embed])

  


client.run(os.getenv('DISCORD_BOT_SECRET'))