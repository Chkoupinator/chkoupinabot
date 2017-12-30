from utils.werewolves import *
from PREFS import prefix


implemented_gamemodes = {
    'carnage': CarnageGame,
    'c': CarnageGame
}


async def execute(chkoupinabot, msg, args):
    if len(args) == 0:
        await msg.channel.send("Only carnage mode is available for now, do `{}werewolf carnage` to start a carnage "
                               "game".format(prefix))
        return
    if msg.guild.id == 345698331500216320 and not (msg.author.top_role.id == 345698700997296138 or  # Elite Aspie
                                                   msg.author.id == 167122174467899393):            # Chkoupinator
        await msg.channel.send("You must be an <@&345698700997296138> or Chkoupinator to start a game. ")
        return
    somme_class_exists = False
    try:
        somme_class_exists = True
        some_class = implemented_gamemodes[args[0]]
    except KeyError:
        await msg.channel.send("Game mode doesn't exist/ hasn't been added yet. Please do `{}werewolf carnage` to start"
                               " a carnage game".format(prefix))
    if somme_class_exists:
        await some_class.initialize(chkoupinabot, msg, args)
