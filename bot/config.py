from ConfigParser import SafeConfigParser
from bot.misc import pretty_dump


class ReportBotConfig(object):
    def __init__(self, config_path):
        self.parser = self._get_parser(config_path)
        self.bot = self._parse_bot_section()
        self.resource = self._parse_resource_section()
        self.dooray = self._parse_dooray_section()

    def __repr__(self):
        return '* mealbot:\n%s\n* dooray:\n%s' % (self.mealbot, self.dooray)

    def _get_parser(self, config_path):
        parser = DefaultConfigParser()
        parser.optionxform = str
        if not parser.read(config_path):
            raise ValueError('No config file found!', config_path)
        return parser

    def _parse_bot_section(self):
        section = 'bot'
        name = self.parser.get(section, 'name')
        msg = self.parser.get(section, 'message')
        return BotConfig(name, msg)

    def _parse_resource_section(self):
        section = 'resource'
        store = self.parser.get(section, 'store')
        container = self.parser.get(section, 'container', container='')
        face_object = self.parser.get(section, 'face-object', face_object=None)
        pic_object = self.parser.get(section, 'pic-object', pic_object=None)
        return ResourceConfig(store, container, face_object, pic_object)

    def _parse_dooray_section(self):
        section = 'dooray'
        hook = self.parser.get(section, 'hook-url', hook=None)
        return DoorayConfig(hook)


class BotConfig(object):
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def __repr__(self):
        retval = dict()
        retval['name'] = self.name
        retval['message'] = self.message
        return pretty_dump(retval)

    def get_name(self):
        return self.name

    def get_message(self):
        return self.message


class ResourceConfig(object):
    def __init__(self, store, container, face_object, pic_object):
        self.store = store
        self.container = container
        self.face_object = face_object
        self.pic_object = pic_object

    def __repr__(self):
        retval = dict()
        retval['store'] = self.store
        retval['container'] = self.container
        retval['face_object'] = self.face_object
        retval['pic_object'] = self.pic_object
        return pretty_dump(retval)

    def get_container_url(self):
        return '/'.join([self.store, self.container])

    def get_face_url(self):
        return '/'.join([self.store, self.container, self.face_object])

    def get_pic_url(self):
        return '/'.join([self.store, self.container, self.pic_object])


class DoorayConfig(object):
    def __init__(self, hook_url):
        self.hook_url = hook_url

    def __repr__(self):
        return self.hook_url


class DefaultConfigParser(SafeConfigParser):
    """
    how to use:
        var = get(section, option, var=default_value)
    """
    def get(self, section, option, **kv):
        return SafeConfigParser.get(self, section, option, raw=True,
                                    vars=DefaultOption(self, section, **kv))

    def getboolean(self, section, option, **kv):
        value = self.get(section, option, **kv)
        if type(value) == bool:
            return value
        elif value and value.lower() in ['yes', 'true']:
            return True
        elif value and value.lower() in ['no', 'false']:
            return False
        else:
            raise TypeError

    def getint(self, section, option, **kv):
        return int(self.get(section, option, **kv))

    def getfloat(self, section, option, **kv):
        return float(self.get(section, option, **kv))

    def getlist(self, section, option, **kv):
        value = self.get(section, option)
        try:
            return list(filter(None, (x.strip() for x in value.splitlines())))
        except Exception:
            return kv


class DefaultOption(dict):
    def __init__(self, config, section, **kv):
        self._config = config
        self._section = section
        dict.__init__(self, **kv)

    def items(self):
        _items = []
        for option in self:
            if not self._config.has_option(self._section, option):
                _items.append((option, self[option]))
            else:
                value_in_config = self._config.get(self._section, option)
                _items.append((option, value_in_config))
        return _items
