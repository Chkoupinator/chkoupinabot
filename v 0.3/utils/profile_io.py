import json
import time
import os


async def loader(msg, user):
    try:
        with open(os.path.join("profiles",str(user.id) + ".json"), 'r') as profile_file:
            return json.load(profile_file)
    except FileNotFoundError:
        if msg.author == user:
            await msg.channel.send("You do not have a profile yet. Generating one with the base values.")
        else:
            await msg.channel.send("User {} does not have a profile yet. Generating one with the base values.".format(
                                                                                                             str(user)))
        with open(os.path.join("profiles", str(user.id) + ".json"), 'w+') as profile_file:
            json.dump({
                "description": "You know nothing about me, brother \n~~mada mada~~",
                "name": user.display_name,
                "avatar": user.avatar_url,
                "age": "Unknown",
                "gender": "Apache Attack Helicopter",
                "region": "Unknown",
                "games": [],
                "main lang": "EN",
                "languages": [],
                "skills": [],
                "fav genres": [],
                "additional info": "",
                "link": "",
                # things that are set by the bot only :
                "achievements": [],
                "exp": 0,
                "created at": time.gmtime()
            }, profile_file, indent=4)
        with open(os.path.join("profiles", str(user.id) + ".json"), 'r') as profile_file:
            return json.load(profile_file)


def saver(profile, userid):
    with open(os.path.join("profiles", str(userid) + ".json"), 'w') as profile_file:
        json.dump(profile, profile_file,  indent=4)
        profile_file.truncate()


async def prettyprinter(channel, user):
    profile = await loader(channel, user)
    saver(profile, user.id)
