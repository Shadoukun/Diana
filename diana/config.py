import configparser


class ConfigManager(object):

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.readfp(open("diana.conf"))

        self._host = self.config.get('general', 'host')
        self._guidelineCounter = self.config.get('general', 'guideline_count')
        self._discordToken = self.config.get('tokens', 'discord')
        self._flaskSecret = self.config.get('tokens', 'flask_secret')
        self._flickrPublic = self.config.get('tokens', 'flickr_public')
        self._flickrSecret = self.config.get('tokens', 'flickr_secret')
        self._wolframToken = self.config.get('tokens', 'wolfram')
        self._wordnikToken = self.config.get('tokens', 'wordnik')

    # # Tokens

    # discord API token

    @property
    def discordToken(self):
        return str(self._discordToken)

    @discordToken.setter
    def discordToken(self, value):
        self.config.set('tokens', 'discord', value)
        self._discordToken = value

    # flask secret key

    @property
    def flaskSecret(self):
        return str(self._flaskSecret)

    @flaskSecret.setter
    def flaskSecret(self, value):
        self.config.set('tokens', 'flask_secret', value)
        self._flaskSecret = value

    # flickr keys

    @property
    def flickrPublic(self):
        return self.config.get('tokens', 'flickr_public')

    @flickrPublic.setter
    def flickrPublic(self, value):
        self.config.set('tokens', 'flickr_public', value)
        self._flickrPublic = value

    @property
    def flickrSecret(self):
        return self.config.get('tokens', 'flickr_secret')

    @flickrSecret.setter
    def flickrSecret(self, value):
        self.config.set('tokens', 'flickr_secret', value)
        self._flickrSecret = value

    # wolfram API token

    @property
    def wolframToken(self):
        return self.config.get('tokens', 'wolfram')

    @wolframToken.setter
    def wolframToken(self, value):
        self.config.set('tokens', 'flickr_secret', value)
        self._wolframToken = value

    # wordnik API token

    @property
    def wordnikToken(self):
        return self.config.get('tokens', 'wordnik')

    @wordnikToken.setter
    def wordnikToken(self, value):
        self.config.set('tokens', 'wordnik', value)
        self._wordnikToken = value

    @property
    def guidelineCounter(self):
        return self.config.get('general', 'guideline_count')

    @guidelineCounter.setter
    def guidelineCounter(self, value):
        self.config.set('general', 'guideline_count', value)
        self._guidelineCounter = value

    @property
    def host(self):
        return self._host


config = ConfigManager()
