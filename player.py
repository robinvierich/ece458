import constants

class Player():

    def __init__(self, sid):
        self._sid = sid
        self._pos = [0,0]
        self._health = 100
        self._gold = 0
        self._equippedItem = None
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
    def equipped_weapon(self):
        return self._equipped_weapon

    @equipped_weapon.setter
    def equipped_weapon(self, value):
        self._equipped_weapon = value


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


    def attack(self, other):
        damage = self.equipped_weapon.damage
        other.health -= damage


    def use_potion(self, potion_name):
        potions = [potion for potion in self.potions if potion.name == potion_name]

        if len(potions) > 0:
            potion = potions[0]
            self.potions.remove(potion)
            self.health += self.potions.heal


