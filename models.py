class Weapon():
    def __init__(self, name="default_weapon", price=0, damage=0):
        self.name = name
        self.price = price
        self.damage = damage

class Potion():
    def __init__(self, name="default_potion", price=0, heal=0):
        self.name = name
        self.price = price
        self.heal = heal
