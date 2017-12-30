import discord
from discord.ext import commands
import PREFS
from cmds import ping, test, emojify, profile, setprofile, werewolf
import asyncio


cmdmap = {
    "ping": ping,
    "chkouping": ping,
    "test": test,
    "emojify": emojify,
    "profile": profile,
    "setprofile": setprofile,
    "werewolf": werewolf,
    "wwg": werewolf

}

public_commands = [
    "ping",
    "test",
    "emojify",
    "profile",
    "setprofile"
]
chkoupinabot = commands.Bot(description=PREFS.description, command_prefix="chkoupinabot;;!")


@chkoupinabot.event
async def on_ready():
    print('Logged in')
    print('Name : {}'.format(chkoupinabot.user.name))
    print('ID : {}'.format(chkoupinabot.user.id))
    print(discord.__version__)


# --------------------------------------------------------Commands------------------------------------------------------


def help_builder():
    help_list = list()
    for cmd in public_commands:
        help_list.append("**`"+PREFS.prefix+cmd+"` : **"+cmdmap[cmd].description)
    embed = discord.Embed(title=PREFS.title, description=PREFS.description, color=discord.Colour.from_rgb(28, 214, 209))
    embed.set_thumbnail(url=chkoupinabot.user.avatar_url)
    embed.add_field(name="Commands list :", value='\n'.join(help_list))
    return embed


@chkoupinabot.command(pass_context=True)
async def chkouping(ctx):
    """To chkouping or not to chkouping, that is the question"""
    await ctx.send("Chkoupong !")


@chkoupinabot.event
async def on_message(msg):
    if not msg.author.bot:
        if msg.content.startswith(PREFS.prefix):
            command = msg.content.lower().split(" ")[0].replace(PREFS.prefix, "")
            if command == "help":
                try:
                    await msg.channel.send(cmdmap[msg.content.lower().split(" ")[1]].help_message)
                except IndexError:
                    await msg.channel.send(embed=help_builder())
            else:
                try:
                    args = msg.content.replace(PREFS.prefix + command, "").split(" ")
                    if args[0] == '':
                        args.remove('')
                    new_args = []
                    add_next_arg = False
                    n = 0
                    for x in args:
                        if add_next_arg:
                            if x.endswith('"'):
                                new_args[n] = " ".join([new_args[n], x])
                                add_next_arg = False
                                n += 1
                            else:
                                new_args[n] = " ".join([new_args[n], x])
                        elif x.startswith('"'):
                            new_args.append(x)
                            add_next_arg = True
                        else:
                            new_args.append(x)
                            n += 1
                    await cmdmap[command].execute(chkoupinabot, msg, new_args)
                except KeyError:
                    possible_commands = ["Command not recognized"]
                    for key in cmdmap.keys():
                        if command in key and len(key.replace(command, "")) < 3:
                            if len(possible_commands) == 1:
                                possible_commands.append("did you mean **`{}{}`**".format(PREFS.prefix, key))
                            else:
                                possible_commands.append("**`{}{}`**".format(PREFS.prefix, key))
                    if len(possible_commands) != 0:
                        if len(possible_commands) > 2:
                            await msg.channel.send(
                                " or ".join([", ".join(possible_commands[0:-1]), possible_commands[-1]]) + "?")
                        elif len(possible_commands) == 2:
                            await msg.channel.send(", ".join(possible_commands) + "?")
        if "huh, really?" in msg.content.lower():
            huhreally = discord.File(fp='huhreally.png', filename='huh really.png')
            await msg.channel.send("", file=huhreally)
        for sentence in PREFS.respond.keys():
            if sentence in msg.content.lower():
                await msg.channel.send(PREFS.respond[sentence])
        if "yamete kudasai" in msg.content.lower():
            if len(msg.mentions) >0:
                for i in range(200):
                    await asyncio.sleep(0.5)
                    await msg.channel.send("yamete kudasai, "+msg.mentions[0].mention)
    await chkoupinabot.process_commands(msg)


chkoupinabot.run(PREFS.HKEY)
