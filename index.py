import discord, os, asyncio
from discord.ext import commands
from dispatcher import dispatch
import config

client = commands.Bot(
    command_prefix = config.BOT['PREFIX'],
    case_insensitive = True
)

@client.event
async def on_ready():
    print('Logged in as {0}'.format(client.user.name))
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "you"))
    
@client.event
async def on_message(msg):
    if msg.author.id != client.user.id and not msg.author.bot and msg.guild and checkLevel(msg.author) != 'none':
        
        if msg.attachments or msg.embeds or (msg.content.__contains__('cdn.') or msg.content.__contains__('media.')):
            await dispatch(msg)
        else:
            print('found no embeds/attachments in message')
            
    await client.process_commands(msg)

    
@client.command(name = 'blacklist', help = 'Adds word to the blacklist', aliases = ['bl', 'ban', 'banword'])
async def blacklist(ctx, msg):
    if checkLevel(ctx.message.author) == 'admin':
        config.BLACKLISTED.append(str(msg.lower()))
        await ctx.send(embed = discord.Embed(title="Blacklisted", description=f'Added `{msg.lower()}` to the blacklist configuration.', colour=discord.Color.green()))
 
@client.command(name = 'unblacklist', help = 'Removes word from the blacklist', aliases = ['unbl', 'ubk', 'unbanword', 'unban'])
async def unblacklist(ctx, msg):
    if checkLevel(ctx.message.author) == 'admin':
        config.BLACKLISTED.remove(str(msg.lower()))
        await ctx.send(embed = discord.Embed(title="Unblacklisted", description=f'Removed `{msg.lower()}` from the blacklist configuration.`', colour=discord.Color.red()))
    
@client.command(name = 'listblacklist', help = 'Lists all blacklisted words', aliases = ['listbl', 'lbl', 'bannedwords'])
async def listblacklist(ctx):
    if checkLevel(ctx.message.author) == 'admin':
        await ctx.send(embed = discord.Embed(title="Blacklist Config", description=f'Blacklist config: \n`{config.BLACKLISTED}`.', colour=discord.Color.purple ()))

@client.command(name = 'whitelist', help = 'Adds allowed roles/people to be ignored by Theia', aliases = ['wl', 'ignore'])
async def whitelist(ctx, user : discord.Member):
    if checkLevel(ctx.message.author) == 'admin':
        config.WUSERS.append(user.id)
        await ctx.send(embed = discord.Embed(title="Whitelisted", description=f'Added `{user.id}` to the whitelist configuration.', colour=discord.Color.green()))
    
@client.command(name = 'unwhitelist', help = 'Removes allowed roles/people to be ignored by Theia', aliases = ['unwl', 'uwk', 'unignore'])
async def unwhitelist(ctx, user : discord.Member):
    if checkLevel(ctx.message.author) == 'admin':
        config.WUSERS.remove(user.id)
        await ctx.send(embed = discord.Embed(title="Unwhitelisted", description=f'Removed `{user.id}` from the whitelist configuration.`', colour=discord.Color.red()))

@client.command(name = 'listwhitelist', help = 'Lists all whitelisted users/roles', aliases = ['listwl', 'lwl', 'ignoredusers'])
async def listwhitelist(ctx):
    if checkLevel(ctx.message.author) == 'admin':
        await ctx.send(embed = discord.Embed(title="Whitelist Config", description=f'Whitelist config: \nUsers : `{config.WUSERS}`', colour=discord.Color.purple ()))


@client.command(name = 'ping', help = 'Fetches the bot\'s ping')
async def ping(ctx):
    await ctx.reply(f'Ping: {round(client.latency, 2)}ms')

def checkLevel(user):
    if user.guild_permissions.manage_messages:
        return 'admin'
    elif searchList(config.WUSERS, str(user.id)):
        return 'whitelisted'
    else:
        return 'none'
    
    
def searchList(list, element):
    for Element in list:
        if Element.__contains__(element):
            return True
    return False


client.run(config.BOT['TOKEN'])