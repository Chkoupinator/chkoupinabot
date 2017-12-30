import discord
from PREFS import prefix
from utils import profile_io
from utils.custom_exceptions import *

description = "Shows your profile, creates one with default values if you don't have one"

help_message = "Shows you your profile or the profile of a person you @mention.\n__**Usage :**__\n```{}profile [" \
               "@mention]```\nIf there is an `@mention` shows you the profile of the @mentioned user, else shows " \
               "your profile.".format(prefix)

too_many_args = "Error, this command only takes 0 or 1 argument. Please do **`{0}help profile`** for more info.\nDid " \
                "you maybe mean **`{0}setprofile`**".format(prefix)

not_a_mention = "Error, the argument you specified isn't a user mention. Please do @name and select one of the " \
                "results or use <@userid> to get a valid user mention. "


async def execute(chkoupinabot, msg, args):
    try:
        if len(args) == 0:
            user = msg.author
            profile = await profile_io.loader(msg, user)
        elif len(msg.mentions) == 1:
            user = msg.mentions[0]
            if user.bot:
                raise UserIsABot
            profile = await profile_io.loader(msg, user)
        else:
            if len(args) > 1:
                raise TooManyArgs
            if len(args) > 0 and len(msg.mentions) == 0:
                raise NotAMention
    except TooManyArgs:
        await msg.channel.send(too_many_args)
        return
    except NotAMention:
        await msg.channel.send(not_a_mention)
        return
    except UserIsABot:
        await msg.channel.send("Us bots cannot have a profile, enjoy your human privilege human! :angrycry:")
        return

    embed = discord.Embed(title=profile["name"], url=profile["link"], description=profile["description"],
                          color=user.colour)
    embed.set_author(name="User profile for " + str(user))
    embed.set_thumbnail(url=profile["avatar"])
    embed.add_field(name="Age : ", value=profile["age"], inline=True)
    embed.add_field(name="Gender : ", value=profile["gender"], inline=True)
    embed.add_field(name="Region : ", value=profile["region"], inline=True)
    embed.add_field(name="Main Language : ", value=profile["main lang"], inline=True)
    if len(profile["fav genres"]) > 0:
        embed.add_field(name="Favorite Genres : ",
                        value="- "+"\n- ".join(str(profile["fav genres"]).split("', '")).replace(
                            "'", '').replace('[', '').replace(']', ''), inline=True)
    if len(profile["languages"]) > 0:
        embed.add_field(name="Languages : ",
                        value="- " + "\n- ".join(str(profile["languages"]).split("', '")).replace(
                            "'", '').replace('[', '').replace(']', ''), inline=True)
    if len(profile["additional info"]) > 0:
        embed.add_field(name="Additional Info : ", value=profile["additional info"], inline=True)
    embed.add_field(name="Level", value="0", inline=True)
    if len(profile["achievements"]) != 0:
        embed.add_field(name="Achievements :", value=profile["achievements"], inline=True)
    embed.set_footer(text="bottom text")
    await msg.channel.send(embed=embed)
