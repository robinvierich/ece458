import constants

class Player():

    def __init__(self, sid):
        self._sid = sid
        self._position = [0,0,0]
        self._health = 100
        self._gold = 0
        self._items = []
        self._resources = []


    @property
    def sid(self):
        return self._sid


    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value


    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value


    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value


    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value


    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = value


