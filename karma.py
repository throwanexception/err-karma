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
        except KeyError:
            stored_karma = {}
            self['karma'] = stored_karma
            self.log.debug('Karma storage was empty, initializing')

        karmed_words = []
        frm = str(message.frm).split('!')[0]
        self.log.debug("Message FRM: {}".format(frm))
        for word in message.body.split():
            word = word[:64]
            if word[:-2] == frm:
                    continue
            if word.endswith('++'):
                word = word[:-2]
                if word in stored_karma.keys(): stored_karma[word] += 1
                else: stored_karma[word] = 1
                karmed_words.append(word)
            elif: word.endswith('--'):
                word = word[:-2]
                if word in stored_karma.keys(): stored_karma[word] -= 1
                else: stored_karma[word] = -1
                karmed_words.append(word)
            else:
                continue

        self['karma'] = stored_karma
        self.log.debug("karmed_words = {}".format(karmed_words))
        self.log.debug("self['karma'] = {}".format(self['karma']))
        if len(karmed_words) == 1:
            word = karmed_words[0]
            karma = self['karma'][word]
            reply = "{} karma is now {}".format(word, karma)
            if karma % 25 == 0:
                self.log.info("{} gets a levelup for {}".format(word, karma))
                self._draw_unicorn(message,reply)
                return True
        elif: len(karmed_words) > 1:
            reply = "{} have just pimped various karma".format(frm)
        else:
            return True
        self.send(message.frm, reply, message)
        return True

    def _draw_unicorn(self, message, extra):
        unicorn = """
{}
     _______\)%%%%%%%%._              
    `''''-'-;   % % % % %'-._         
            :b) \            '-.      
            : :__)'    .'    .'       
            :.::/  '.'   .'           
            o_i/   :    ;             
                   :   .'             
                    ''`
""".format(extra)
        self.send(message.frm, unicorn, message)

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def srank(self, mess, args):
        self.log.info("Processing SRANK with args: {}".format(args))
        try:
            karma = self['karma']
        except KeyError:
            karma = {}

        sorted_karma = sorted(karma.items(), key=operator.itemgetter(1), reverse=True)
        rank = ""
        for elem in sorted_karma[0:10]:
            rank += "{} {}\n".format(elem[0], elem[1])
        return rank

    @botcmd
    def _draw(self, mess, args):
        self._draw_unicorn(mess)
        return True
