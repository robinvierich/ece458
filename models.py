class Weapon():
    def __init__(self, name="default_weapon", price=0, damage=0):
        self.name = name
        self.price = price
        self.damage = damage

    def __repr__(self):
        return '%s $%s dmg=%s' % (self.name, self.price, self.damage)

class Potion():
    def __init__(self, name="default_potion", price=0, heal=0):
        self.name = name
        self.price = price
        self.heal = heal

    def __repr__(self):
        return '%s $%s heal=%s' % (self.name, self.price, self.heal)
