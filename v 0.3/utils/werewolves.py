from utils.custom_exceptions import *
import random
import discord
import asyncio
import time

invite_error_timeout = 60
ready_timeout = 120
open_join_timeout = 300


class Ability:
    abilities_dict = dict()

    def __init__(self, name, description):
        self.name = name
        self.description = description
        Ability.abilities_dict[name] = self


class Card:
    cards_list = list()
    vote = Ability('Vote', 'Every day villagers can vote to hang someone they suspect is a werewolf')

    def __init__(self, name, side, description):
        self.name = name
        self.side = side
        self.description = description
        Card.cards_list.append(self)
        self.abilities = [Card.vote]

    def description_embed(self):
        embed = discord.Embed(name=self.name, description=self.description)
        embed.set_author(name="Information about your card :")
        embed.add_field(name='Alignment:', value=self.side)
        embed.add_field(name='Abilities:',
                        value='- ' + '\n- '.join(ability.name + ': ' + ability.description for ability in
                                                 self.abilities), inline=False)
        embed.set_thumbnail(url=self.image_url)
        return embed


class Player:
    players_list = list()

    def __init__(self, user, card):
        self.user = user
        self.name = user.display_name
        self.card = card
        self.sides = [card.side]
        self.alive = True
        self.soul_mate = None


class Werewolf(Card):
    players = list()
    devour = Ability('Devour', 'Each night werewolves can decide to devour someone.')
    card_abilities = [devour]
    image_url = \
        'https://images-cdn.asmodee.us/filer_public/ce/4c/ce4ceb3f-a5b9-422b-ae7e-d0dd6165b78f/loups-garous_b.jpg'

    def __init__(self):
        super().__init__('Werewolf', 'werewolves', 'Werewolves are unwillingly evil and dangerous creatures, at day '
                                                   'they are simple humans doing their simple life. But when the night '
                                                   'falls, they transform to humanoid wolves with an incredible hunger'
                                                   'and a strong craving for human flesh.\n'
                                                   'Their goal is to devour every last villager.')
        self.abilities.extend(Werewolf.card_abilities)


class WerewolfPlayer(Player):
    def __init__(self, user):
        Player.__init__(self, user=user, card=Werewolf())
        Werewolf.players.append(self)
        self.card = Werewolf()


class Sorceress(Card):
    players = list()
    death_potion = Ability('Death Potion', "A single potion that could put an end to someone's life")
    protective_potion = Ability('Protective Potion', "A single potion that could protect someone from getting devoured")
    card_abilities = [death_potion, protective_potion]
    image_url = 'https://www.jeuxetcompagnie.fr/wp-content/uploads/2011/11/sorciere3.jpg'

    def __init__(self):
        super().__init__('Sorceress', 'village', "The Sorceress is a wicked character that can play with the life and "
                                                 "death of the villagers. She has two powerful potions and she can "
                                                 "use one or both at any night she wants. One of them puts an end to "
                                                 "someone's life, the other prevents someone from having their life put"
                                                 " to and end by the werewolves.\n"
                                                 "As a villagers' friend, she tries to use her potions to kill the foul"
                                                 " creatures known as werewolves hidden among the inhabitants of her "
                                                 "village.")
        self.abilities.extend(Sorceress.card_abilities)


class SorceressPlayer(Player):
    def __init__(self, user):
        Player.__init__(self, user=user, card=Sorceress())
        Sorceress.players.append(self)
        self.card = Sorceress()


class Cupid(Card):
    players = list()
    love_arrows = Ability('Love Arrows', "Two arrows to make two people in love. If one of them dies, the other "
                                         "suicides")
    card_abilities = [love_arrows]
    image_url = 'https://www.jeuxetcompagnie.fr/wp-content/uploads/2011/11/cupidon3.jpg'

    def __init__(self):
        super().__init__('Cupid', 'villager', "Cupid is a vicious character who can play with people's heart. He came t"
                                              "o the village to spread love in the village by using his magical arrows."
                                              " The two persons hit by his arrow become deeply in love, so deeply that "
                                              "if any of them dies, the other will not be able to endure the suffering "
                                              "and will end their life too.\n"
                                              "After using his two arrows cupid becomes a normal villager and has to "
                                              "survive the werewolves and help the village get rid of them.")
        self.abilities.extend(Cupid.card_abilities)


class CupidPlayer(Player):
    def __init__(self, user):
        Player.__init__(self, user=user, card=Cupid())
        Cupid.players.append(self)
        self.card = Cupid()


class Psychic(Card):
    players = list()
    crystal_ball = Ability('Crystal Ball', "Every night, the crystal ball can show the true nature of someone.")
    card_abilities = [crystal_ball]
    image_url = 'https://www.jeuxetcompagnie.fr/wp-content/uploads/2011/11/voyante1.jpg'

    def __init__(self):
        super().__init__('Psychic', 'villager', "The Psychic is a powerful and mighty woman. When the night comes, she "
                                                "can use her magical artifact to spy on someone she chooses. With it, "
                                                "she can see the true nature of anyone in the village.\n"
                                                "As a regular woman her artifact aside, the psychic needs to survive "
                                                "from the werewolves' hunger and put an end to them.")
        self.abilities.extend(Psychic.card_abilities)


class PsychicPlayer(Player):
    def __init__(self, user):
        Player.__init__(self, user=user, card=Psychic())
        Psychic.players.append(self)
        self.card = Psychic()


class Hunter(Card):
    players = list()
    last_breath = Ability('Last Breath', "When your time comes. Extend it by enough time to kill someone you chose.")
    card_abilities = [last_breath]
    image_url = 'https://www.jeuxetcompagnie.fr/wp-content/uploads/2011/11/chasseur2.jpg'

    def __init__(self):
        super().__init__('Hunter', 'villager', "The hunter is a man with an iron will and a heavily trained body. If he"
                                               " gets killed by anyone, he can use his last breath to take his trusted "
                                               "rifle and land a shot right between the eyes of someone of his choosing"
                                               ", ending their life instantly.\n"
                                               "His goal is to help the villagers and hunt every last werewolf in the "
                                               "village.")
        self.abilities.extend(Hunter.card_abilities)


class HunterPlayer(Player):
    def __init__(self, user):
        Player.__init__(self, user=user, card=Hunter())
        Hunter.players.append(self)
        self.card = Hunter()


class Game:
    players = list()
    in_game_users = list()


class CarnageGame:
    running_games = list()
    nplayers = 6

    def __init__(self, game_role, game_channel, players_dict):
        self.players = list(players_dict.values())
        self.players_dict = players_dict
        Game.players.extend(players_dict.keys())
        self.role = game_role
        self.channel = game_channel
        self.players_names_dict = dict()
        self.werewolves = list()
        self.cupid = None
        self.sorceress = None
        self.psychic = None
        self.hunter = None
        for player in self.players:
            self.players_names_dict[player.name.lower()] = player
            if isinstance(player.card, Werewolf):
                self.werewolves.append(player)
            elif isinstance(player.card, Cupid):
                self.cupid = player
            elif isinstance(player.card, Sorceress):
                self.sorceress = player
            elif isinstance(player.card, Psychic):
                self.psychic = player
            elif isinstance(player.card, Hunter):
                self.hunter = player
        self.dead_players = list()
        self.alive_villagers = [self.cupid, self.sorceress, self.hunter, self.psychic]
        self.nights = 0
        self.days = 0
        CarnageGame.running_games.append(self)

    def get_alive_villagers(self):
        x = list(self.alive_villagers)
        random.shuffle(x)
        return x

    async def player_quit(self, user):
        player = self.players_dict[user]
        await player.wwg_personal_role.remove()
        await player.user.remove_roles(self.role)
        del self.players_dict[user]
        Game.players.remove(player)
        Game.in_game_users.remove(user)

    async def end_of_game(self, *, log=False):
        CarnageGame.running_games.remove(self)
        if log:
            messages = await self.channel.history(limit=None, reverse=True)
        await self.channel.category.delete(reason='Game Over')
        await self.channel.delete(reason='Game Over')
        await self.role.delete(reason='Game Over')
        for player in self.players:
            await player.wwg_personal_role.remove()
        if log:
            return messages

    def alive_players(self):
        x = list(self.alive_villagers)
        x.extend(self.werewolves)
        random.shuffle(x)
        return x

    def alive_players_minus_player(self, player):
        x = list(self.alive_players())
        x.remove(player)
        return x

    def alive_cards(self):
        alive_cards = {}
        for player in self.players:
            card = player.card
            if card not in alive_cards.keys():
                alive_cards[card] = 1
            else:
                alive_cards[card] += 1
        return alive_cards

    async def night(self, chkoupinabot):
        await self.channel.send("**The night falls ...**")

        if self.nights == 0:
            await self.channel.send("**Cupid is selecting his target ...**")
            await self.cupid.user.send(
                "Since this is carnage you are obliged to shoot an arrow at yourself. You have 30 seconds to select "
                "whomst's knees are getting a love arrow. Possible targets:" +
                "; ".join(p.name for p in self.alive_players_minus_player(self.cupid)) +
                "\nTo select someone simply send a message with their name (and nothing else).")

            try:
                def valid_target(m):
                    return m.content.lower().replace('"', '') in list(self.players_names_dict.keys()) \
                           and isinstance(m.channel, discord.DMChannel) and m.channel.recipient == self.cupid.user and \
                                self.players_names_dict[m.content.lower().replace('"', '')] is not self.cupid
                cupid_message = await chkoupinabot.wait_for('message', timeout=30, check=valid_target)
                target = self.players_names_dict[cupid_message.content.lower().replace('"', '')]
            except asyncio.TimeoutError:
                target = random.choice(self.alive_players_minus_player(self.cupid))
                await self.cupid.user.send("You took too much time to select a target has been selected randomly.")
            await self.cupid.user.send("Sending sum love to " + target.name + ".")
            target.soul_mate = self.cupid
            self.cupid.soul_mate = target
            await target.user.send("Cupid **({})** hit you with a love arrow! You are now bound for life but more "
                                   "importantly, for *death*.".format(self.cupid.name))

            #

            await self.channel.send("**The Sorceress is using her death potion ...**")
            await self.sorceress.user.send(
                "Since this is carnage you are obliged to use your potion on the first night. You have 30 seconds to "
                "select a person to poison. Possible targets:" +
                "; ".join(p.name for p in self.alive_players_minus_player(self.sorceress)) +
                "\nTo select someone simply send a message with their name (and nothing else).")

            try:
                def valid_target(m):
                    return m.content.lower().replace('"', '') in list(self.players_names_dict.keys()) \
                           and isinstance(m.channel, discord.DMChannel) and m.channel.recipient == self.sorceress.user \
                           and self.players_names_dict[m.content.lower().replace('"', '')] is not self.cupid
                sorceress_message = await chkoupinabot.wait_for('message', timeout=30, check=valid_target)
                poison_target = self.players_names_dict[sorceress_message.content.lower().replace('"', '')]
            except asyncio.TimeoutError:
                poison_target = random.choice(self.alive_players_minus_player(self.sorceress))
                await self.sorceress.user.send("You took too much time to select a target has been selected randomly.")
            await self.sorceress.user.send(poison_target.name + " will not wake up tomorrow.")
            self.werewolves_channel = await self.channel.guild.create_text_channel(category=self.channel.category,
                                                                                   name='werewolf_channel')

        await self.channel.send("**The werewolves are selecting someone to devour ...**")
        await self.werewolves_channel.set_permissions(self.channel.guild.default_role, read_messages=False)
        await self.werewolves_channel.set_permissions(self.role, read_messages=False)
        for werewolf in self.werewolves:
            await self.werewolves_channel.set_permissions(werewolf.user, read_messages=True, send_messages=True)
        await self.werewolves_channel.send("@everyone. You have now two minute to decide for someone to eat, you "
                                           "can also become vegetarian for tonight and select nobody. Targets are: "
                                           "" + "; ".join(player.name for player in self.get_alive_villagers()) + "\n"
                                           + 'Select someone by typing `select <Player Name>` you can remove your '
                                             'selection with `unselect`.\nIf you are two alive, you will have to settle'
                                             ' on one single target.')
        werewolf_target = None
        for werewolf in self.werewolves:
            werewolf.tmp_target = None
        try:
            vote_start = time.time()

            while werewolf_target is None:
                if 180-(time.time()-vote_start) < 0:
                    raise asyncio.TimeoutError

                def valid_target(m):
                    who = None
                    for player in self.alive_villagers:
                        if m.content.lower().replace('select ', '') == player.name.lower():
                            who = player
                    return m.channel == self.werewolves_channel and (('select' in m.content.lower() and who is not None)
                                                                    or 'unselect' in m.content.lower()) or \
                           (180-(time.time()-vote_start) < 0)

                msg = await chkoupinabot.wait_for('message', check=valid_target, timeout=120)
                if 180-(time.time()-vote_start) < 0:
                    raise asyncio.TimeoutError
                player_author = self.players_dict[msg.author]
                if 'unselect' in msg.content.lower():
                    player_author.tmp_target = None
                else:
                    player_author.tmp_target = self.players_names_dict[msg.content.lower().replace('select ', '')]
                    await self.werewolves_channel.send(
                        player_author.name+" wants to eat "+player_author.tmp_target.name+"\n" +
                        str(int(120-(time.time() - vote_start)))+" seconds left until the vote time is out.")

                if len(self.werewolves) == 2 and self.werewolves[0].tmp_target == self.werewolves[1].tmp_target:
                    werewolf_target = self.werewolves[0].tmp_target
                elif len(self.werewolves) == 1 and self.werewolves[0].tmp_target is not None:
                    werewolf_target = self.werewolves[0].tmp_target

        except asyncio.TimeoutError:
            if len(self.werewolves) > 1 and self.werewolves[0].tmp_target != self.werewolves[1].tmp_target:
                if self.werewolves[0].tmp_target is None:
                    werewolf_target = self.werewolves[1].tmp_target
                elif self.werewolves[1].tmp_target is None:
                    werewolf_target = self.werewolves[0].tmp_target
                else:
                    await self.werewolves_channel.send("Times up!")

        if len(self.werewolves) == 2:
                if self.werewolves[0].tmp_target is None and self.werewolves[1].tmp_target is None:
                    await self.werewolves_channel.send("Time's up! You didn't chose anyone so vegan is the way!"
                                                       " Nobody will be devoured this night.")

                if self.werewolves[0].tmp_target != self.werewolves[1].tmp_target:
                    await self.werewolves_channel.send("Time's up! You selected two different targets so no "
                                                       "devouring for you! Better get along with your mates next time.")
        if len(self.werewolves) == 1 and self.werewolves[0].tmp_target is None :
            await self.werewolves_channel.send("Time's up! You didn't chose anyone so vegan is the way!"
                                               " Nobody will be devoured this night.")

        else:
            await self.werewolves_channel.send(werewolf_target.name+" is the chosen one, you will now feast on them in "
                                                                    "their sleep.")
        for werewolf in self.werewolves:
            await self.werewolves_channel.set_permissions(werewolf.user, read_messages=True, send_messages=False)

        #

        await self.channel.send("**The psychic will now use her crystal ball ...**")
        await self.psychic.user.send("Select someone to look up with your crystal ball. The card you find will be "
                                     "revealed to everyone in the game (without giving names). Possible targets are: " +
                                     "; ".join(player.name for player in self.get_alive_villagers()) + "\n"
                                     "To select someone simply send their name (and nothing else) in a message.")
        try:
            def valid_target(m):
                return m.content.lower().replace('"', '') in list(self.players_names_dict.keys()) \
                       and isinstance(m.channel, discord.DMChannel) and m.channel.recipient == self.psychic.user and \
                       self.players_names_dict[m.content.lower().replace('"', '')] in self.alive_villagers

            psychic_message = await chkoupinabot.wait_for('message', timeout=30, check=valid_target)
            target = self.players_names_dict[psychic_message.content.lower().replace('"', '')]
            await self.psychic.user.send("**"+target.name+"** is a "+target.card.name)
            await self.channel.send("The psychic saw someone who is a **"+target.card.name+"**")
        except asyncio.TimeoutError:
            await self.psychic.user.send("Time's out! You will not look anyone for tonight ...")

        self.nights += 1
        try:
            if werewolf_target == poison_target:
                return [werewolf_target]
            else:
                return [werewolf_target, poison_target]
        except:
            return [werewolf_target]

    async def day(self, chkoupinabot):
        await self.channel.send("It's time to hang the evil werewolves! But who are they?! You can vote to hang someone"
                                " even if you don't know! Type `vote_hang @<Player Name>` to vote for someone, or "
                                "remove your vote by typing `vote_hang nobody`\n You have 3 minutes.")
        await self.channel.set_permissions(self.role, read_messages=True, send_messages=True)
        hanging_dict = {}
        for player in self.alive_players():
            hanging_dict[player] = 0

        try:

            vote_start = time.time()

            while True:
                if 180-(time.time()-vote_start) < 0:
                    raise asyncio.TimeoutError

                def valid_target(m):
                    return (m.channel == self.channel and ('vote_hang' in m.content.lower() and (len(m.mentions) == 1
                            and m.mentions[0] in list(self.players_dict.keys()) and self.players_dict[m.mentions[0]] in
                            self.alive_players())) or ('nobody' in m.content.lower())) or \
                                                                                    (180-(time.time()-vote_start) < 0)
                msg = await chkoupinabot.wait_for('message', check=valid_target)
                if 180-(time.time()-vote_start) < 0:
                    raise asyncio.TimeoutError
                player_author = self.players_dict[msg.author]
                if 'nobody' in msg.content.lower():
                    try:
                        hanging_dict[player_author.hang_target] -= 1
                    except:
                        pass
                    player_author.hang_target = None
                else:
                    try:
                        hanging_dict[player_author.hang_target] -= 1
                    except:
                        pass
                    player_author.hang_target = self.players_dict[msg.mentions[0]]
                    hanging_dict[player_author.hang_target] += 1
                    await self.channel.send(player_author.name+" votes against "+player_author.hang_target.user.mention+
                                            ", which now has **"+str(hanging_dict[player_author.hang_target])+
                                            "** votes against him/her.\n"+str(int(180-(time.time()-vote_start)))+
                                            " seconds left until the vote time is out.")

        except asyncio.TimeoutError:
            pass
        await self.channel.send("Time's up!")

        def keywithmaxval(d):
            """ a) create a list of the dict's keys and values;
                b) return the key with the max value"""
            v = list(d.values())
            k = list(d.keys())
            return k[v.index(max(v))]
        hanging_target = keywithmaxval(hanging_dict)
        await self.channel.set_permissions(self.role, read_messages=True, send_messages=False)
        await self.channel.send("The village decided to hang "+hanging_target.user.mention+" who was a " +
                                hanging_target.card.name)
        self.days += 1
        return hanging_target

    async def start(self, chkoupinabot):
        embed = discord.Embed(title="Carnage Werewolf game!",
                              description="Quick recap of the rules in a carnage game:\n"
                                          " - The sorceress only has a poison potion that she is forced to use on the "
                                          "first night.\n"
                                          " - The hunter is forced to kill someone when he dies.\n"
                                          " - The cupid is forced to target himself in the couple.\n"
                                          "Your card and its description have been sent in to your DMs!",
                              color=discord.Colour.red())
        embed.set_thumbnail(url='https://images-cdn.asmodee.us/filer_public/ce/4c/ce4ceb3f-a5b9-422b-ae7e-'
                                'd0dd6165b78f/loups-garous_b.jpg')
        await self.channel.send(embed=embed)
        for player in self.players:
            await player.user.send(embed=embed)
            await player.user.send(embed=player.card.description_embed())
        while len(self.alive_villagers) > 0 and len(self.werewolves) > 0 and not (len(self.alive_players()) == 2
                                                                                    and self.cupid.alive and
                                                                                        self.cupid.soul_mate.alive):
            deaths = await self.night(chkoupinabot)
            morning_deads_message = "@everyone The morning sun rises,  **"
            for dead in deaths:
                if dead in self.alive_villagers:
                    self.alive_villagers.remove(dead)
                morning_deads_message = morning_deads_message + dead.name + "** the **" + dead.card.name + "**, **"
            morning_deads_message = morning_deads_message + "*however, will not wake up ...***"
            await self.channel.send(morning_deads_message)
            suicide = None
            if self.cupid in deaths and self.cupid.soul_mate not in deaths:
                suicide = self.cupid.soul_mate
            elif self.cupid.soul_mate in deaths and self.cupid not in deaths:
                suicide = self.cupid
            if suicide is not None:
                await self.channel.send("Out of sadness, for **"+suicide.soul_mate.name+"**'s death, **"+suicide.name +
                                        "** the **"+suicide.card.name+"** decided to put an end to their life.")
                deaths.append(suicide)
            if self.hunter in deaths:
                await self.channel.send(
                    "Reassembling his last few bits of strength, the Hunter  takes up his trusted rifle and prepares "
                    "to shoot. "+self.hunter.user.mention+", you have 30 seconds  to select a target from: " +
                    "; ".join(player.name for player in self.alive_players()) +
                    " by typing `select @<Player Name>`.")
                await self.channel.set_permissions(self.hunter.user, send_messages=True)
                try:
                    def valid_target(m):
                        return m.channel == self.channel and m.author == self.hunter.user and len(m.mentions) > 0 and \
                               m.mentions[0] in list(self.players_dict.keys()) and self.players_dict[m.mentions[0]] in \
                                                                                                    self.alive_players()
                    shot_message = await chkoupinabot.wait_for('message', timeout=30, check=valid_target)
                    shot = self.players_dict[shot_message.mentions[0]]
                except asyncio.TimeoutError:
                    shot = random.choice(self.alive_players())
                    await self.channel.send("Timeout, choosing someone randomly ...")
                await self.channel.set_permissions(self.hunter.user, send_messages=False)
                await self.channel.send("Bang! "+shot.user.mention+" the "+shot.card.name+" got shot dead on the spot!")
                deaths.append(shot)
            for dead in deaths:
                dead.alive = False
                if dead in self.alive_villagers:
                    self.alive_villagers.remove(dead)
                await dead.wwg_personal_role.edit(name=dead.card.name+" - Dead", colour=discord.Colour.red())
                if dead in self.werewolves:
                    self.werewolves.remove(dead)
                await self.channel.set_permissions(dead.user, send_messages=False)
            if len(self.dead_players) == 0:
                self.deads_channel = await self.channel.guild.create_text_channel(category=self.channel.category,
                                                                                             name='channel-of-the-dead')
            await self.deads_channel.set_permissions(self.channel.guild.default_role, read_messages=False)
            await self.deads_channel.set_permissions(self.role, read_messages=False)
            for dead in deaths:
                await self.deads_channel.set_permissions(dead.user, read_messages=True, send_messages=True)
            self.dead_players.extend(deaths)
            if len(self.werewolves) == 0 or len(self.alive_villagers) == 0 or (len(self.alive_players()) == 2
                                                                                    and self.cupid.alive and
                                                                                        self.cupid.soul_mate.alive):
                break

#           Day

            hanged = await self.day(chkoupinabot)
            deaths = [hanged]
            for dead in deaths:
                if dead in self.alive_villagers:
                    self.alive_villagers.remove(dead)
            if self.hunter in deaths:
                await self.channel.send("Reassembling his last few bits of strength, the Hunter  takes up his trusted "
                                        "rifle and prepares to shoot. "+self.hunter.user.mention+", you have 30 seconds"
                                        " to select a target from: "+"; ".join(player.name for player in
                                        self.alive_players())+" by typing `select @<Player Name>`.")
                await self.channel.set_permissions(self.hunter.user, send_messages=True)
                try:
                    def valid_target(m):
                        return m.channel == self.channel and m.author == self.hunter.user and len(m.mentions) > 0 and \
                               m.mentions[0] in list(self.players_dict.keys()) and self.players_dict[m.mentions[0]] in \
                                                                                                    self.alive_players()

                    shot_message = await chkoupinabot.wait_for('message', timeout=30, check=valid_target)
                    shot = self.players_dict[shot_message.mentions[0]]
                except asyncio.TimeoutError:
                    shot = random.choice(self.alive_players())
                    await self.channel.send("Timeout, choosing someone randomly ...")
                await self.channel.set_permissions(self.hunter.user, send_messages=False)
                await self.channel.send("Bang! "+shot.user.mention+" the "+shot.card.name+" got shot dead on the spot!")
                deaths.append(shot)
            for dead in deaths:
                dead.alive = False
                if dead in self.alive_villagers:
                    self.alive_villagers.remove(dead)
                await dead.wwg_personal_role.edit(name=dead.card.name + " - Dead", colour=discord.Colour.red())
                if dead in self.werewolves:
                    self.werewolves.remove(dead)
                await self.deads_channel.set_permissions(dead.user, read_messages=True, send_messages=True)
        if len(self.werewolves) == 0:
            await self.channel.send("@everyone **The villagers killed all the werewolves and therefore won the game! "
                                    "Congratulations!**")
        elif len(self.alive_villagers) == 0:
            await self.channel.send("@everyone **The werewolves ate everyone and therefore won the game!"
                                    " Congratulations!**")
        elif len(self.alive_players()) == 2 and self.cupid.alive and self.cupid.soul_mate.alive:
            await self.channel.send("**The couple "+self.cupid.user.mention+" and "+self.cupid.soul_mate.user.mention+""
                                    " survived together and therefore won the game! Congratulations!**")

    @staticmethod
    async def initialize(chkoupinabot, msg, args):
        users_list = [msg.author]

        # async def mentions_minus_self(msg):
        #     if msg.author == msg.mentions:
        #         await msg.channel.send("Error: you mentioned yourself! *Removing yourself from the invites.*")
        #         return msg.mentions.remove(msg.author)
        #     else:
        #         return msg.mentions

        async def open_players_join(users_in_lobby):
            await msg.channel.send("The game is now open for everyone to join. Type `join` in this channel to get in!")
            open_spots = CarnageGame.nplayers - len(users_in_lobby)
            try:
                while open_spots > 0:
                    def join(m):
                        return m.channel == msg.channel and 'join' in m.content.lower() and (
                            m.author not in users_in_lobby) and not m.author.bot

                    join_msg = await chkoupinabot.wait_for('message', timeout=open_join_timeout, check=join)
                    users_in_lobby.append(join_msg.author)
                    open_spots -= 1
                    await msg.channel.send("**{}** joined! Players in lobby are: {}. Open spots: {}".format(
                        join_msg.author.display_name, ", ".join(user.display_name for user in users_in_lobby),
                        open_spots))
            except asyncio.TimeoutError:
                await msg.channel.send("Timeout! Not enough players joined the lobby in the {} given minutes. Get "
                                       "some players and come back <:pepe_ok_hand:382198933134245888>".format(
                    str(int(open_join_timeout / 60))))

            return users_in_lobby

        if '-i' in args:

            async def invited_players_ready(invited_players, invite_only):
                await msg.channel.send("{}Players {}, you have two minutes to answer with `ready`!"
                                       "".format(invite_only, ", ".join(user.mention for user in invited_players)))
                users_ready = list()
                users_not_ready = invited_players
                try:
                    while True:
                        def ready(m):
                            return m.author in invited_players and m.channel == msg.channel and (
                                'ready' in m.content.lower()) and m.author not in users_ready and not m.author.bot

                        ready_msg = await chkoupinabot.wait_for('message', timeout=ready_timeout, check=ready)
                        users_ready.append(ready_msg.author)
                        users_not_ready.remove(ready_msg.author)
                        await msg.channel.send("**{}** is ready! Players that confirmed to be ready are: {}. Awaiting "
                                               "for: {}".format(ready_msg.author.display_name,
                                                                ", ".join(user.display_name for user in users_ready),
                                                                ", ".join(user.display_name for user in users_not_ready)
                                                                ))
                        if len(users_not_ready) == 0:
                            break
                except asyncio.TimeoutError:
                    pass
                if len(users_not_ready) == 0:
                    await msg.channel.send("All invited players are ready!")
                else:
                    await msg.channel.send("Time's out! Players {} did not respond, you can still join but your spots "
                                           "are no longer reserved".format(
                        ', '.join(u.display_name for u in users_not_ready)))
                return users_ready

            if len(msg.mentions) < 5:
                await msg.channel.send("Not enough players mentioned would you rather invite {0} more people or open "
                                       "the {0} spots to everyone?\n Type `invite <@mentions of the {0} players you "
                                       "want to invite>` or `open`".format(5 - len(msg.mentions)))
                invited_users = msg.mentions
                try:
                    def valid_answer(m):
                        return m.author == msg.author and m.channel == msg.channel and (
                            'open' in m.content.lower() or 'invite' in m.content.lower())

                    answer = await chkoupinabot.wait_for('message', timeout=invite_error_timeout, check=valid_answer)
                except asyncio.TimeoutError:
                    await msg.channel.send("**Timeout** : No valid answer has been given in 1min, defaulting to "
                                           "open spots")
                try:
                    if 'invite' in answer.content.lower():
                        if len(invited_users) + len(answer.mentions) < 5:
                            invited_users.extend(answer.mentions)
                            raise AttributeError
                        elif len(invited_users) + len(answer.mentions) == 5:
                            invited_users.extend(answer.mentions)
                            users_list.extend(await invited_players_ready(invited_users, "Running invite only mode; "))
                        else:
                            await msg.channel.send("Too many users, defaulting to open spots.")
                            raise AttributeError
                    else:
                        raise AttributeError
                except AttributeError:
                    users_list.extend(await invited_players_ready(invited_users, ''))
                if len(users_list) < 6:
                    await msg.channel.send("Not enough, players. Resorting to open mode.")
                    users_list = await open_players_join(users_list)
            elif len(msg.mentions) > 5:
                await msg.channel.send("Too many players mentioned, would you rather re invite 5 people or open the "
                                       "game to everyone?")
                try:
                    def valid_answer(m):
                        return m.author == msg.author and m.channel == msg.channel and (
                            'open' in m.content.lower() or 'invite' in m.content.lower())

                    answer = await chkoupinabot.wait_for('message', timeout=invite_error_timeout, check=valid_answer)
                except asyncio.TimeoutError:
                    await msg.channel.send("**Timeout**: No valid answer has been given in {}min, defaulting to "
                                           "open spots".format(str(int(invite_error_timeout / 60))))

                invite = False
                try:
                    if 'invite' in answer.content.lower():
                        if len(answer.mentions) < 5:
                            invited_users = answer.mentions
                            invite = True
                            raise AttributeError
                        elif len(answer.mentions) == 5:
                            invited_users = answer.mentions
                            users_list.extend(await invited_players_ready(invited_users, "Running invite only mode; "))
                        else:
                            await msg.channel.send("Too many users, defaulting to open spots.")
                            raise AttributeError
                    else:
                        raise AttributeError
                except AttributeError:
                    if invite:
                        users_list.extend(await invited_players_ready(invited_users, ''))
                if len(users_list) < 6:
                    await msg.channel.send("Not enough, players. Resorting to open mode.")
                    users_list = await open_players_join(users_list)
            else:
                users_list.extend(await invited_players_ready(msg.mentions, "Running invite only mode; "))
                if len(users_list) < 6:
                    await msg.channel.send("Not enough, players. Resorting to open mode.")
                    users_list = await open_players_join(users_list)
        else:
            users_list = await open_players_join(users_list)

        if len(users_list) < 6:
            return
        else:
            game_role = await msg.guild.create_role(name='wwg, carnage (id {})'.format(len(CarnageGame.running_games)
                                                                                       + 1))
            game_category = await msg.guild.create_category(
                name='Carnage Game (ID : {})'.format(len(CarnageGame.running_games) + 1),
                overwrites={msg.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            msg.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                            game_role: discord.PermissionOverwrite(read_messages=True)})
            game_channel = await msg.guild.create_text_channel(
                name='carnage-{}'.format(len(CarnageGame.running_games) + 1),
                category=game_category)
            await game_channel.set_permissions(msg.guild.default_role, send_messages=False, read_messages=False)
            cards_dict = {
                'werewolf1': WerewolfPlayer,
                'werewolf2': WerewolfPlayer,
                'cupid': CupidPlayer,
                'sorceress': SorceressPlayer,
                'psychic': PsychicPlayer,
                'hunter': HunterPlayer
            }
            cards_list = list(cards_dict.keys())
            random.shuffle(cards_list)
            players_dict = {}
            for n in range(len(users_list)):
                user = users_list[n]
                player = cards_dict[cards_list[n]](user)
                players_dict[user] = player
                player.wwg_personal_role = await msg.guild.create_role(name='unknown card - alive',
                                                                       colour= discord.Colour.green())
                player.user = user
                await user.add_roles(game_role, player.wwg_personal_role)
            game = CarnageGame(game_role, game_channel, players_dict)
            for player in players_dict.values():
                player.wwg = game

            await game.start(chkoupinabot)

            def yes_from_chkoupinator(m):
                return m.author.id == 167122174467899393 and 'bot, please delete everything' in m.content.lower() \
                       and m.channel == game.channel
            await chkoupinabot.wait_for('message', check=yes_from_chkoupinator)
            await game.end_of_game()
