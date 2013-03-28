import socket

import constants


class Client():
    def __init__(self):
        self._sock = socket.socket()
        self._sock.connect((constants.HOST, constants.PORT))
        print 'client connected to server'


    def login(self, username, pass_hash):
        self._sock.sendall('login, %s, %s' % (username, pass_hash))


    def logout(self, sID):
        self._sock.sendall('logout, %s' % sID)


    def move(self, sID, relative_pos):
        self._sock.sendall('move, %s, %s' % (sID, relative_pos))


    def equip(self, sID, item):
        self._sock.sendall('equip, %s, %s' % (sID, item))


    def attack(self, sID, target):
        self._sock.sendall('attack, %s, %s' % (sID, target))


    def gather(self, sID, resource):
        self._sock.sendall('gather, %s, %s' % (sID, resource))


    def buy(self, sID, item):
        self._sock.sendall('buy, %s, %s' % (sID, item))


    def sell(self, sID, item):
        self._sock.sendall('sell, %s, %s' % (sID, item))


    def get_visible_player_positions(self, sID):
        self._sock.sendall('get_visible_player_positions, %s, %s' % (sID, item))

