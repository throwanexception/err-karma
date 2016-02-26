from errbot import BotPlugin, botcmd
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
        for word in message.body.split():
            word = word[:64]
            if word.endswith('++'):
                word = word[:-2]
                if word in stored_karma.keys(): stored_karma[word] += 1
                else: stored_karma[word] = 1
                karmed_words.append(word)
            elif word.endswith('--'):
                word = word[:-2]
                if word in stored_karma.keys(): stored_karma[word] -= 1
                else: stored_karma[word] = -1
                karmed_words.append(word)
            else:
                self.send(message.frm, "Too long karmastring.")
                return True

        self['karma'] = stored_karma
        self.log.debug("karmed_words = {}".format(karmed_words))
        self.log.debug("self['karma'] = {}".format(self['karma']))
        if len(karmed_words) == 1:
            word = karmed_words[0]
            reply = "{} karma is now {}".format(word, self['karma'][word])
        else:
            reply = "{} have just pimped various karma".format(message.frm.split('!')[0])
        self.send(message.frm, reply, message)
        return True

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def srank(self, mess, args):
        try:
            karma = self['karma']
        except KeyError:
            karma = {}
        return karma
