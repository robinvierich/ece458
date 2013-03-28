import socket

import constants

class Client():
    def __init__(self):
        self._sock = socket.socket()
        self._sock.connect((constants.HOST, constants.PORT))
        print 'client connected to server'


    def login(self, username, pass_hash):
        self._sock.sendall('login, %s, %s' % (username, pass_hash))
        pass


    def logout(self, sID):
        pass


    def move(self, sID, relative_pos):
        pass


    def equip(self, sID, item):
        pass


    def attack(self, sID, target):
        pass


    def gather(self, sID, resource):
        pass


    def buy(self, sID, item):
        pass


    def sell(self, sID, item):
        pass


    def get_visible_player_positions(self, sID, item):
        pass

