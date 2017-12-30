from PREFS import prefix

description = "Sends a \"Pong !\""
help_message = "You ping, I pong back \n__**Usage :**__\n```{}ping```\nSends a \"Pong!\"".format(prefix)
async def execute(msg, args):
    if "chkou" in msg.content.lower():
        await msg.channel.send('Chkoupong!')
    else:
        await msg.channel.send('Pong!')
