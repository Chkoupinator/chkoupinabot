from utils import profile_io, long_text, short_text, img_url, list_of_text, url
from utils.custom_exceptions import *


description = "sorry description is still being worked on"

help_message = "sorry the help message is still being worked on"


fields_dict = {
                "description": long_text,
                "name": short_text,
                "avatar": img_url,
                "age": short_text,
                "gender": short_text,
                "region": short_text,
                "games": list_of_text,
                "main lang": short_text,
                "languages": list_of_text,
                "skills": list_of_text,
                "fav genres": list_of_text,
                "additional info": long_text,
                "link": url
}


async def execute(chkoupinabot, msg, args):
    try:
        if not len(args):
            raise KeyError
        new_value = fields_dict[args[0].replace('"', '')].get(args[1:])
        print(args[0] + '=' + str(new_value))
        profile = await profile_io.loader(msg, msg.author)
        profile[args[0].replace('"', '')] = new_value
        profile_io.saver(profile, msg.author.id)
        await msg.channel.send("Profile set successfully")
    except KeyError:
        await msg.channel.send("The fields that you can set are : `"+"`, `".join(fields_dict.keys())+"`.")
    except IndexError:
        await msg.channel.send("Error : Not enough input. Please specify what you want in the field you selected.")
    except ShortTextTooLong:
        await msg.channel.send("Error : Input text was too long. The field you specified takes 64 characters at max.")
    except LongTextTooLong:
        await msg.channel.send("Error : Input text was too long. The field you specified takes 512 characters at max.")
    except TooManyArgs:
        await msg.channel.send('Error : Too many arguments. The field you specified only takes one argument.')
    except NotAValidLink:
        await msg.channel.send('Error : Invalid link. The field you selected only takes an http(s) link')
    except NotAValidImage:
        await msg.channel.send('Error : Not an image. Your link needs to be one of a valid image (jpg/png/gif only)')
