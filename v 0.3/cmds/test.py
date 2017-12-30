from PREFS import prefix
from utils import profile_io
import asyncio
import discord

help_message = 'This command is just here for testing. Move along, peasant.\n__**Usage :**__\n```{}test <arg1> <arg2> '\
               '<"arg number 3"> ...```\nMakes the bot send a message with "arg1, arg2, "arg number 3" ..."'\
                                                                                                         .format(prefix)

description = "Is commonly used to test stuff, you can try to figure out what it does <:zoomeyes:393462548713832458>"


async def execute(chkoupinabot, msg, args):
    if "mycolour" in msg.content.lower():
        await msg.channel.send(str(msg.author.colour.to_rgb()))
    elif "pimpmyjson" in msg.content.lower():
        await profile_io.prettyprinter(msg.channel, msg.author)
        await msg.add_reaction(':pepe_ok_hand:382198933134245888')
    elif "asyncfor" in msg.content.lower():
        li = ["foo", "bar", "spam", "more spam"]
        await msg.channel.send("It's guessing time !")
        answers = list()
        try:
            while set(li) != set(answers):
                def ready(m):
                    return m.content.lower() in li and m.author == msg.author
                answer = await chkoupinabot.wait_for('message', timeout=10, check=ready)
                answers.append(answer.content.lower())
                await msg.channel.send("Good guess, {} is in the list".format(answer.content.lower()))
            await msg.channel.send("GG EZ")
        except asyncio.TimeoutError:
            await msg.channel.send("Timeout !")
    elif "clear this shit" in msg.content.lower() and (msg.author == msg.guild.owner
                                                       or msg.author.id == 167122174467899393):
        for channel in list(msg.guild.text_channels):
            if 'carnage' in channel.name or 'werewolf' in channel.name or 'dead' in channel.name:
                await channel.delete()
        for role in list(msg.guild.roles):
            if 'carnage' in role.name or 'unknown card' in role.name or 'Dead' in role.name:
                await role.delete()
        for category in list(msg.guild.categories):
            if 'carnage' in category.name.lower():
                await category.delete()
        await msg.channel.send("<:pepe_ok_hand:382198933134245888>")
    elif "channel test" in msg.content.lower():
        game_category = await msg.guild.create_category(
            name='Test Category',
            overwrites={msg.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        msg.author: discord.PermissionOverwrite(read_messages=True)})
        game_channel = await msg.guild.create_text_channel(
            name='test',
            category=game_category)
        await game_channel.set_permissions(msg.guild.default_role, send_messages=False, read_messages=False)
    elif len(args) > 0:
        await msg.channel.send(", ".join(args))
    else:
        await msg.channel.send("Gimmie some args you dork")
