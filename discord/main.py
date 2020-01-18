import discord   # pip install discord.py
import sched, time
from datetime import timedelta, datetime
import asyncio
import TOKENS

from scoreboard import *
from cyclecount import *

client = discord.Client()
currentCycle = Cycle()

HELP_MSG = "Valid collection names are: " + ", ".join(COLLECTIONS) + "\n"\
           "To report all of today's cycle in the order listed above: $cycle 1,2,3,4,5,6,5,4,3 \n"\
           "To report some of today's cycle: $cycle name,name,...name num,num,...num \n" \
            "\t Example 1: $cycle loom 3 will report heirloom is on cycle 3 \n" \
            "\t Example 2: $cycle flower,loom,egg 3,2,1 will report flower on cycle 3, loom on  2 and egg on 1 \n"\
           "To get a link of the map with today's newest reported cycle list: $maplink \n"

ERR_MSG = "Wrong format. Type $help for supported commands."

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        return

    if message.channel.type is not discord.ChannelType.private:
        return

    if message.content.startswith('$help'):
        await message.channel.send(HELP_MSG)
        return

    if message.content.startswith('$cycle '):
        response = {}
        user_level = 1
        try:
            tokens = message.content.split()[1:]
            if len(tokens) == 1:
                cycle_list = tokens[0].split(",")
                for i, c in enumerate(COLLECTIONS):
                    response[c] = cycle_list[i]
            elif len(tokens) == 2:
                response = zip(tokens[0].split(","), tokens[1].split(","))
            else:
                await message.channel.send(ERR_MSG)
            currentCycle.update(response, user_level)
            await message.channel.send('Updated!')
            return
        except:
            await message.channel.send(ERR_MSG)
        return

    if message.content.startswith('$maplink '):
        currentCycle.check_stats()
        await message.channel.send(currentCycle.verbose())
        return

    if message.content.startswith('$statsdbg '):
        currentCycle.check_stats()
        await message.channel.send(str(currentCycle))
        return

    if message.content.startswith('$'):
        await message.channel.send(ERR_MSG)

@client.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = '{0.mention}, Welcome to {1.name}! PM me $help to read all the commands.'.format(member, guild)
        await guild.system_channel.send(to_send)

if __name__ == "__main__":
    cycle_loop = sched.scheduler(time.time, time.sleep)

    def reset_cycle(start_time):
        print("reset")
        currentCycle = Cycle()
        utcnow = datetime.utcnow()
        utctomorrow = (datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        next_start_time = start_time + utctomorrow.timestamp() - utcnow.timestamp()
        cycle_loop.enterabs(next_start_time, 1, reset_cycle, argument=(next_start_time,))
    reset_cycle(time.time())

    #cycle_loop.run()
    client.run(TOKENS.token)