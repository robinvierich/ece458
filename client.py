import socket

import constants


class Client():
    def __init__(self):
        self._sock = socket.socket()
        self._sock.connect((constants.HOST, constants.PORT))
        self._sid = None
        print 'client connected to server'


    def login(self, username, pass_hash):
        self._sock.sendall('login; %s; %s' % (username, pass_hash))

        data = self._sock.recv(4096)
        if data == '':
            raise Exception('socket broken');

        self._sid = data

    def __check_sid(self):
        if self._sid == None:
            raise Exception('cannot send message. login first')


    def logout(self):
        self.__check_sid()

        self._sock.sendall('logout; %s' % self._sid)


    def move(self, relative_pos):
        self.__check_sid()

        self._sock.sendall('move; %s; %s' % (self._sid, relative_pos))


    def equip(self, item):
        self.__check_sid()

        self._sock.sendall('equip; %s; %s' % (self._sid, item))


    def attack(self, target):
        self.__check_sid()

        self._sock.sendall('attack; %s; %s' % (self._sid, target))


    def use_potion(self, potion_name):
        self.__check_sid()

        self._sock.sendall('use_potion; %s; %s' % (self._sid, potion_name))


    def get_visible_map_positions(self):
        self.__check_sid()

        self._sock.sendall('get_visible_map_positions; %s' % self._sid)

