class User():
    def __init__(self, username="default_user", pass_hash="default_pass"):
        self.username = username
        self.pass_hash = pass_hash


class Item():
    def __init__(self, id=0, name="default_item", price=0, damage=0):
        self.id = id
        self.name = name
        self.price = 0
        self.damage = 0

class Resource():
    def __init__(self, id=0, name="default_resource", price=0, heal=0):
        self.id = id
        self.name = name
        self.price = 0
        self.heal = 0
