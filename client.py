import socket
import ssl

import constants


class Client():
    def __init__(self):
        self._sock = socket.socket()
        self._sock = ssl.wrap_socket(self._sock, cert_reqs=ssl.CERT_NONE)
        self._sock.connect((constants.CLIENT_HOST, constants.CLIENT_PORT))
        self._sid = None
        print 'client connected to server'


    def login(self, username, pass_hash):
        self._sock.sendall('login; %s; %s' % (username, pass_hash))

        data = self._sock.recv(4096)
        if data == '':
            raise Exception('socket broken')

        self._sid = data

    def __check_sid(self):
        if self._sid == None:
            raise Exception('cannot send message. login first')

    def show_player(self):
        self.__check_sid()

        self._sock.sendall('show_player;%s' % self._sid)

        data = self._sock.recv(4096)
        if data == '':
            raise Exception('socket broken')

        return data


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


    def show_map(self):
        self.__check_sid()

        self._sock.sendall('show_map; %s' % self._sid)

        data = self._sock.recv(4096)
        if data == '':
            raise Exception('socket broken')

        #visible_map = '\n'.join([str(row) for row in eval(data)])
        visible_map = eval(data)
        return visible_map
