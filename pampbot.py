import discord
from discord.ext import commands
import requests
import os

TOKEN = os.environ.get('TOKEN')
PAMP_URL='https://cdn.discordapp.com/attachments/801133693946953730/929866107953741824/PAMP.gif'
OPENSEA_BASE_URL='https://api.opensea.io/api/v1/'

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    # call the process_commands routine as we are overriding the default on_message behavior
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@bot.command(name='pamp')
async def pamp(ctx):
    await ctx.send(PAMP_URL)

@bot.command(name='collection')
async def collection(ctx, collection, more=None):
    url = OPENSEA_BASE_URL + "collection/" + collection
    resp = requests.get(url)
    if resp.status_code != 200:
        print("failed to retrieve data from opensea")
        return
    stats = resp.json()['collection']['stats']

    myEmbed = discord.Embed(title=collection, description=resp.json()['collection']['external_url'], color=0x00ff00)
    if more != None:
        for name, stat in stats.items():
            myEmbed.add_field(name=constant.OPENSEA_STATS[name], value=stat, inline=False)
    else:
        myEmbed.add_field(name="Total Volume", value=stats['total_volume'], inline=False)
        myEmbed.add_field(name="Floor Price", value=stats['floor_price'], inline=False)
        myEmbed.add_field(name="One Day Sales", value=stats['one_day_sales'], inline=False)
        myEmbed.add_field(name="One Day Average Price", value=stats['one_day_average_price'], inline=False)
        myEmbed.add_field(name="Average Price", value=stats['average_price'], inline=False)

    await ctx.send(embed=myEmbed)

bot.run(TOKEN)
