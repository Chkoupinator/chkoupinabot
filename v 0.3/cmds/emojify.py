from PREFS import prefix
emoji_alphabet = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
                  'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
                  'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿', '$': '💲', '#': '#⃣', '*': '*⃣', '!': '❕',
                  '?': '❔'}


def emojifier(args):
    emojified_text = ""
    for character in args:
        if character.lower() in emoji_alphabet:
            emojified_text = emojified_text + emoji_alphabet[character.lower()] + " "
        else:
            if character == " ":
                emojified_text = emojified_text + "   "
            else:
                emojified_text = emojified_text + character
    return emojified_text


help_message = "Returns the text input written with emojis \n__**Usage :**__\n```{}emojify <text>```\nTransforms the " \
               "`<text>` into 🇹🇪🇽🇹".format(prefix)

description = "Transforms a text to a 🇹🇪🇽🇹, ain't that great?"


async def execute(chkoupinabot, msg, args):
    await msg.channel.send(emojifier(msg.content.lower().replace("{}emojify ".format(prefix), "")))
