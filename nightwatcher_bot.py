import asyncio
import discord
import htmlScrape
import tanklookup as tl
import userlimits
import markupdatejob as marks
import os
from datetime import datetime, timedelta


client = discord.Client()
wot_regions = {'!na', '!eu', '!ru', '!sea'}
wot_channels = {'hidden-channel', 'wot-uncensored', 'wot', 'bot-stuff', 'temp-wot-channel'}
limits = []
marks_last_updated = datetime.utcnow()
mark_dictionary = marks.get_marks_heap()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global limits
    limits = userlimits.userlimits('userlimits.txt')


@client.event
async def on_disconnect():
    userlimits.filewrite('userlimits.txt', limits)


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name not in wot_channels:
        return

    command = message.content.split(' ', 1)

    if command[0].lower() in wot_regions:
        if message.channel.name != 'bot-stuff':
            if not userlimits.checklimit(limits, message.author.id):
                await message.channel.send(f"<@{message.author.id}> has run out of stat lookups today <:KappaPeek:681704630408970311>")
                return
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

    elif command[0].lower() == '!tank':
        answer = tl.tanklookup(command[1])
        await message.channel.send(answer)

    elif command[0].lower() == '!compare':
        command = command[1].split(', ', 10)
        answer = tl.tankcompare(command)
        await message.channel.send(answer)

    elif command[0].lower() in ['!namark', '!eumark', '!rumark']:
        global marks_last_updated
        region = command[0].lower()[1:3]
        if (marks_last_updated + timedelta(days=1)) < datetime.utcnow():
            loop = asyncio.get_event_loop()
            answer = await loop.run_in_executor(None, tl.lookup_mark_heap, command[1], region, mark_dictionary, True)
        else:
            answer = tl.lookup_mark_heap(command[1], region, mark_dictionary)
        await message.channel.send(answer)


print('Bot starts')
client.run(os.environ.get('KEY', None))
