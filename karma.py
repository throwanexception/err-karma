# This is a skeleton for Err plugins, use this to get started quickly.

from errbot import BotPlugin, botcmd


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

        karmed_words = {}
        for word in message.body.split():
            if word.endswith('++'):
                word = word[:-2]
                if word in karmed_words.keys(): karmed_words[word] += 1
                else: karmed_words[word] = 1
            if word.endswith('--'):
                word = word[:-2]
                if word in karmed_words.keys(): karmed_words[word] -= 1
                else: karmed_words[word] = -1
        stored_karma.update(karmed_words)
        self['karma'] = stored_karma
        self.log.debug("karmed_words = {}".format(karmed_words))
        self.log.debug("self['karma'] = {}".format(self['karma']))
        if len(karmed_words) == 1:
            word = karmed_words.keys()[0]
            return "{} karma is now {}".format(word, self['karma'][word])
        else:
            return "{} just pimped various karma".format(message.frm)

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def srank(self, mess, args):
        try:
            karma = self['karma']
        except KeyError:
            karma = {}
        return karma
