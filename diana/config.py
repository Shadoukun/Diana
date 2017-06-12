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

    # discord API token

    @property
    def discordToken(self):
        return str(self._discordToken)

    # flask secret key

    @property
    def flaskSecret(self):
        return str(self._flaskSecret)

    # flickr keys

    @property
    def flickrPublic(self):
        return str(self._flickrPublic)

    @property
    def flickrSecret(self):
        return str(self._flickrSecret)

    # wolfram API token

    @property
    def wolframToken(self):
        return str(self._wolframToken)

    # wordnik API token

    @property
    def wordnikToken(self):
        return str(self._wordnikToken)

    # Host

    @property
    def host(self):
        return str(self._host)


config = ConfigManager()
