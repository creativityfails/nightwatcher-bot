import asyncio
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
async def on_disconnect():
    print('Bot disconnect')


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name not in wot_channels:
        return

    command = message.content.split(' ', 1)

    if command[0].lower() in wot_regions:
        loop = asyncio.get_event_loop()
        command = message.content.split(' ', 3)
        if len(command) == 3:
            answer = await loop.run_in_executor(None, htmlScrape.wotlabs_scrape, command[0][1:].lower(),
                                                command[1], command[2].lower())
            await message.channel.send(answer)
        else:
            answer = await loop.run_in_executor(None, htmlScrape.wotlabs_scrape, command[0][1:].lower(),
                                                command[1])
            await message.channel.send(answer)

    if command[0].lower() == '!tank':
        answer = tl.tanklookup(command[1])
        await message.channel.send(answer)

    if command[0].lower() == '!compare':
        command = command[1].split(', ', 10)
        answer = tl.tankcompare(command)
        await message.channel.send(answer)


client.run(botkey.key)
