import constants

class Player():

    def __init__(self, sid, health=100):
        self._sid = sid
        self._pos = [0, 0]
        self._health = health
        self._equipped_weapon = None
        self._weapons = []
        self._potions = []

    def __str__(self):
        return """
        Player State:
        sid = %s
        pos = %s
        health = %s
        equipped = %s
        weapons = %s
        potions = %s
        """% (self.sid, self.pos, self.health, 
                self.equipped_weapon, self.weapons, self.potions)

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

    def try_equip(self, weapon_name):
        for weapon in self.weapons:
            if weapon.name == weapon_name:
                self._equipped_weapon = weapon
                return weapon

    @property
    def weapons(self):
        return self._weapons

    @weapons.setter
    def weapons(self, value):
        self._weapons = value


    @property
    def potions(self):
        return self._potions

    @potions.setter
    def potions(self, value):
        self._potions = value


    def attack(self, other):
        if self.equipped_weapon == None:
            return

        damage = self.equipped_weapon.damage
        other.health -= damage


    def use_potion(self, potion_name):

        for potion in self.potions:
            print 'potion: ', potion
            if potion.name == potion_name:
                self.health += potion.heal
                self.potions.remove(potion)
                break




