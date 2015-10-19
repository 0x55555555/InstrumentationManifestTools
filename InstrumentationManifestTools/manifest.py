import collections
import uuid
import hashlib


class ManifestBase:
    """
    Base to all nameable objects in the manifest.
    """

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """
        Identifier for the object
        """
        return self._name


class Profile(ManifestBase):
    def __init__(self, name, gui_name):
        super(Profile, self).__init__(name)
        self._providers = []
        self._gui_name = gui_name

    def add(self, providers, **kwargs):
        self._providers.append((providers, kwargs))

    @property
    def gui_name(self):
        return self._gui_name

    @property
    def providers(self):
        return self._providers


class Provider(ManifestBase):
    """
    Base object which provides instrumentation for an executable
    """

    def __init__(self, name, **kwargs):
        super(Provider, self).__init__(name)
        self.contents = collections.defaultdict(lambda: [])
        self._next_value = 1
        self._binary_filename = kwargs["binary_filename"]

    def add(self, obj):
        container = self.contents[obj.__class__.__name__.lower()]
        container.append(obj)

        obj.assign_value(self._next_value)
        self._next_value += 1

    def container(self, name):
        if (name in self.contents):
            return self.contents[name]

        return []

    @property
    def guid(self):
        m = hashlib.md5()
        m.update(bytearray(self.name, 'utf8'))
        uuid_bytes = m.digest()
        return '{%s}' % uuid.UUID(bytes=uuid_bytes)

    @property
    def binary_filename(self):
        return self._binary_filename


class ItemBase(ManifestBase):
    def __init__(self, name, **kwargs):
        super(ItemBase, self).__init__(name)
        self._message = kwargs.get("message", None)
        self._value = 0

    def assign_value(self, value):
        if hasattr(self.__class__, 'minimum_id'):
            value += self.__class__.minimum_id
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def message(self):
        return self._message


class Event(ItemBase):
    def __init__(self, name, **kwargs):
        super(Event, self).__init__(name)

        self._channel = kwargs.get("channel", None)
        self._task = kwargs.get("task", None)
        self._opcode = kwargs.get("opcode", None)
        self._keywords = kwargs.get("keywords", None)
        self._level = kwargs.get("level", None)
        self._template = kwargs.get("template", None)

    @property
    def channel(self):
        return self._channel

    @property
    def task(self):
        return self._task

    @property
    def opcode(self):
        return self._opcode

    @property
    def keywords(self):
        return self._keywords

    @property
    def level(self):
        return self._level

    @property
    def template(self):
        return self._template


class Task(ItemBase):
    pass


class Opcode(ItemBase):
    minimum_id = 10


class Keyword(ItemBase):
    def __init__(self, name, **kwargs):
        super(Keyword, self).__init__(name)
        self._mask = kwargs["mask"]

    @property
    def mask(self):
        return self._mask


class Filter(ItemBase):
    @property
    def template(self):
        return None


class Level(ItemBase):
    minimum_id = 16


class Template(ItemBase):
    def __init__(self, name, **kwargs):
        super(Template, self).__init__(name)
        self._data = []

    def add_data(self, name, type):
        self._data.append((name, type))

    @property
    def data(self):
        return self._data


class Channel(ItemBase):
    def __init__(self, name, **kwargs):
        super(Channel, self).__init__(name)
        self._type = kwargs.get("type", "Operational")

    @property
    def enabled(self):
        return True

    @property
    def type(self):
        return self._type
