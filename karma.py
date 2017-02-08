from errbot import BotPlugin, botcmd
import operator
# -*- coding: utf-8 -*-

class Karma(BotPlugin):
    """An Err karma plugin"""

    def callback_message(self, message):
        """Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour"""
        try:
            stored_karma = self['karma']
        except (KeyError, TypeError):
            stored_karma = {}
            self['karma'] = stored_karma
            self.log.debug('Karma storage was empty, initializing')

        try:
            blacklist = self.config['blacklist']
        except (KeyError, TypeError):
            blacklist = []
        try:
            ignore_users = self.config['ignore_users']
        except (KeyError, TypeError):
            ignore_users = []

        karmed_words = []
        frm = str(message.frm).split('!')[0]
        self.log.debug("Message FRM: {}".format(frm))
        if frm in ignore_users:
            self.log.info("Ignoring karma adjustment from blacklisted user: {}".format(frm))
            return True
        for word in message.body.split():
            word = word[:64]
            if word[:-2] == frm:
                    self.send(message.to, 
                    "Public masturbation is not allowed, {}".format(frm), message)
                    continue
            if word.endswith('++'):
                word = word[:-2]
                if word and word not in blacklist:
                    if word in stored_karma.keys(): stored_karma[word] += 1
                    else: stored_karma[word] = 1
                    karmed_words.append(word)
                else:
                    self.log.info("Unwanted word occured: {}".format(word))
            elif word.endswith('--'):
                word = word[:-2]
                if word and word not in blacklist:
                    if word in stored_karma.keys(): stored_karma[word] -= 1
                    else: stored_karma[word] = -1
                    karmed_words.append(word)
                else:
                    self.log.info("Unwanted word occured: {}".format(word))
            else:
                continue

        self['karma'] = stored_karma
        self.log.debug("karmed_words = {}".format(karmed_words))
        self.log.debug("self['karma'] = {}".format(self['karma']))
        if len(karmed_words) == 1:
            word = karmed_words[0]
            karma = self['karma'][word]
            reply = "{} karma is now {}".format(word, karma)
            if karma % 25 == 0 and karma > 0:
                self.log.info("{} gets a levelup for {}".format(word, karma))
                self._draw_unicorn(message,reply)
                return True
        elif len(karmed_words) > 1:
            reply = "{} have just pimped various karma".format(frm)
        else:
            return True
        self.send(message.to, reply, message)
        return True

    def get_configuration_template(self):
        conf = { 'blacklist': ["word1", "word2"], 'ignore_users': ["user1", "user2"] }
        return conf

    def check_configuration(self, config):
        self.log.debug("Called check_configuration with: {}".format(config))
        # TODO: check the configuration here
        return True

    def _draw_unicorn(self, message, extra):
        unicorn = """
1UP! {}

     _______\)%%%%%%%%._              
    `''''-'-;   % % % % %'-._         
            :b) \            '-.      
            : :__)'    .'    .'       
            :.::/  '.'   .'           
            o_i/   :    ;             
                   :   .'             
                    ''`
""".format(extra)
        self.send(message.to, unicorn, message)

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd
    def srank(self, mess, args):
        """Shows top 10 karma rankings"""

        self.log.info("Processing SRANK with args: {}".format(args))
        try:
            karma = self['karma']
        except KeyError:
            karma = {}
            return "I don't have any karma stored yet."

        rank = "Top 10: "
        if args:
            rank = ""
            for elem in set(args.split()):
                rank += "{}({}) ".format(elem, karma.get(elem, 0))
        else:
            sorted_karma = sorted(karma.items(), key=operator.itemgetter(1), reverse=True)
            for elem in sorted_karma[0:10]:
                rank += "{}({}) ".format(elem[0], elem[1])
        return rank
