import discord

from cycle import Cycle
import settings
import TOKENS
import score


class PostOfficerClient(discord.Client):
    def __init__(self, cycle, score_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cycle = cycle
        self.score_obj = score_obj
        self.scoreboard = None

    def run(self, *args, **kwargs):
        self.scoreboard = self.score_obj()
        super().run(*args, **kwargs)

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = '{0.mention}, Welcome to {1.name}! PM me $help to read all the commands.'.format(member, guild)
            await guild.system_channel.send(to_send)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if self.scoreboard.get(message.author.id) is None:
            self.scoreboard.add_element(message.author.id)

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
            return

        # if message.channel.type is not discord.ChannelType.private:
        #     return

        if message.content.startswith('$help'):
            await message.channel.send(settings.HELP_MSG)
            return

        if message.content.startswith('$cycle '):
            user_level = self.scoreboard.get(message.author.id, "reputation")[0] // 10
            try:
                tokens = message.content.split()[1:]
                score_generated = 0
                if len(tokens) == 1:
                    score_generated = self.cycle.update(zip(settings.COLLECTIONS, tokens[0].split(",")), user_level)
                elif len(tokens) == 2:
                    score_generated = self.cycle.update(zip(tokens[0].split(","), tokens[1].split(",")), user_level)
                else:
                    await message.channel.send(settings.ERR_MSG)
                    return
                self.scoreboard.add_to_value(message.author.id, "reputation", score_generated)
                await message.channel.send(settings.UPDATED_MSG.format(score_generated))
                return
            except:
                await message.channel.send(settings.ERR_MSG)
            return

        if message.content.startswith('$maplink'):
            await message.channel.send(self.cycle.verbose())
            return

        if message.content.startswith('$rep'):
            await message.channel.send(str(message.author) + settings.REP_MSG + str(self.scoreboard.get(message.author.id)[1]))
            return

        if message.content.startswith('$statsdbg'):
            self.cycle.update_stats()
            await message.channel.send(str(self.cycle))
            return

if __name__ == "__main__":
    testClient = PostOfficerClient(cycle=Cycle())
    testClient.run(TOKENS.token)
