import discord
import htmlScrape
import tanklookup as tl
import botkey

client = discord.Client()
wot_regions = {'!na', '!eu', '!ru', '!sea'}
wot_channels = {'hidden-channel', 'wot-uncensored', 'wot'}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content.split(' ', 1)

    if command[0].lower() in wot_regions and message.channel.name in wot_channels:
        command = message.content.split(' ', 3)
        if len(command) == 3:
            answer = htmlScrape.wotlabs_scrape(command[0][1:].lower(), command[1], command[2].lower())
        else:
            answer = htmlScrape.wotlabs_scrape(command[0][1:].lower(), command[1])
        await message.channel.send(answer)

    if command[0].lower() == '!tank':
        answer = tl.tanklookup(command[1])
        await message.channel.send(answer)

    if command[0].lower() == '!compare':
        command = message.content.split(' ', 10)
        answer = tl.tankcompare(command[1:])
        await message.channel.send(answer)

client.run(botkey.key)
