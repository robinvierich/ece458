import socket
import threading
import select
import random

import constants
from player import Player
from models import Potion, Weapon

#{ session id : player }
sid_to_player_map = {}

users = {
    'admin': 'admin',
}

potions = { 
    'weak'  : Potion('weak', price=10, heal=10),
    'medium': Potion('medium', 20, 25),
    'strong': Potion('strong', 30, 40),
}


weapons = { 
    'club' : Weapon('club', price=10, damage=10),
    'sword': Weapon('sword', 20, 25),
    'staff': Weapon('staff', 30, 40),
}


game_map = [
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
]


xmax = len(game_map) - 1
ymax = len(game_map[0]) - 1

class Server(threading.Thread):
    def __init__(self, host=constants.HOST, port=constants.PORT):
        threading.Thread.__init__(self)
        self._running = False
 
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow reusing same address (errors if another sock still open from previous run)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((host, port))
        self._sock.listen(1)
        self._sock.setblocking(0.0)

        print 'server: server thread created'

    def _handle_request(self, socket, data):
        print 'server: in _handle_request'

        split_data = data.split(";");

        method_name = "handle_%s" % split_data[0].strip()

        if not hasattr(self, method_name):
            print "server: ERROR! got bad method_name: ", method_name
            return

        method = getattr(self, method_name)

        # ** login is a special case
        if method_name == 'handle_login':

            username, pass_hash = split_data[1:]

            sid = self.handle_login(socket, username, pass_hash)
            socket.sendall(str(sid))

        elif len(split_data) > 2:
            args = split_data[1:]
            method(*args)

        elif len(split_data) > 1:
            args = split_data[1].strip()
            method(args)
        else:
            method()


    def handle_login(self, socket, username, pass_hash):
        print 'server: in handle login. %s, %s, %s' % (socket, username, pass_hash)
        stored_pass_hash = users.get(username)

        sid = random.random()

        if pass_hash == stored_pass_hash:
            sid_to_player_map[sid] = Player(sid)

        return sid


    def handle_logout(self, sid):
        print 'server: in handle logout. %s'% sid
        if sid in sid_to_player_map:
            del sid_to_player_map[sid]


    def handle_move(self, sid, relative_pos_str):
        print 'server: in handle move. %s, %s'% (sid, str(relative_pos_str))
        player = sid_to_player_map.get(sid)
        if player == None:
            return

        relative_pos = eval(relative_pos_str)

        player.pos[0] += relative_pos[0]
        player.pos[1] += relative_pos[1]

        # make sure player isn't outside bounds
        player.pos[0] = min(max(player.pos[0], xmin), xmax)
        player.pos[1] = min(max(player.pos[1], ymin), ymax)

        x, y = player.pos

        game_cell = game_map[x][y]

        if not game_cell == ' ':
            # try add weapon
            weapon = weapons.get(game_cell)
            if weapon:
                player.weapons.append(weapon)
                return

            # try add potion
            potion = potions.get(game_cell)
            if potion:
                player.potions.append(potion)
                return

            # not weapon/potion, must be other player
            pass


    def handle_equip(self, sid, weapon):
        print 'server: in handle equip. %s, %s'% (sid, weapon)
        player = sid_to_player_map.get(sid)
        if player == None:
            return
        player.equipped_weapon = weapon


    def handle_attack(self, sid, target_id):
        print 'server: in handle attack. %s, %s'% (sid, target_id)
        player = sid_to_player_map.get(sid)
        if player == None:
            return

        target = sid_to_player_map[target_id]
        player.attack(target)


    def handle_use_potion(self, sid, potion_name):
        print 'server: in handle_use_potion. %s, %s'%  (sid, potion_name)
        player = sid_to_player_map.get(sid)
        if player == None:
            return

        player.use_potion(potion_name)


    def handle_get_visible_map(self, sid):
        print 'server: in handle get_visible_player_positions. %s'% (sid)
        player = sid_to_player_map.get(sid)
        if player == None:
            return

        #TODO: make this work

        return game_map


    def run(self):
        print 'server: server thread started'

        self._running = True

        sock_list = [self._sock]

        while self._running:
            try:
                readable_socks, writable_socks, err_socks = select.select(sock_list, [], [], 1.0)
            except socket.timeout as e:
                print 'got normal (non-error) timeout ', e
                continue

            for sock in readable_socks:

                # if there's a new connection coming in (self._sock state changed)
                if sock is self._sock:
                    connected_socket, client_address = self._sock.accept() # blocks waiting for connection
                    print 'server: got connection from ', client_address

                    sid = connected_socket.getpeername()
                    sock_list.append(connected_socket)

                #if there's data coming in (another socket's state changed)
                else:
            #        try:
                    data = sock.recv(constants.BUFFER_SIZE)
                    real_sid = sock.getpeername()

                    if data:
                        print 'server: received data from ', client_address
                        print 'server: data = ', data
                        self._handle_request(sock, data)
                    else:
                        print 'server: no more data from ', client_address
                        sock.close()
                        sock_list.remove(sock)
                        break

                    #except Exception as e:
                        #print 'server: Connection ERROR! ', e
                        #sock.close()

    def stop(self):
        print 'server: stopping server thread'
        self._running = False
        print 'server: joining server thread'
        self.join()
        print 'server: server thread joined'


