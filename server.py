import socket
import ssl
import threading
import select
import random
import os

import time

import constants
from player import Player
from models import Potion, Weapon

#{ session id : player }

def get_sid():
    sid = 0
    while True:
        sid += 1
        yield sid

time.clock()

sid_generator = get_sid()

enemy_sid = sid_generator.next()

sid_to_player_map = {
    enemy_sid : Player(enemy_sid)
}

sock_to_request_time = {}

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
    'staff': Weapon('staff', 30, 100),
}


game_map = [
        [' ',     ' ',      'club', ' ',     ' '     ],
        [' ',     ' ',      ' ',    ' ',     'weak'  ],
        [' ',     ' ',      ' ',    ' ',     ' '     ],
        ['staff', ' ',      ' ',    'sword', ' '     ],
        [' ',     'medium', ' ',    ' ',     'strong'],
]



xmax = len(game_map) - 1
ymax = len(game_map[0]) - 1

class Server(threading.Thread):
    def __init__(self, host=constants.SERVER_HOST, port=constants.SERVER_PORT):
        threading.Thread.__init__(self)
        self._running = False
 
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow reusing same address (errors if another sock still open from previous run)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((host, port))
        self._sock.listen(1)
        self._sock.setblocking(0.0)


        print 'server: server thread created'


    def _update_game_map(self):
        for player in sid_to_player_map.values():
            x, y = player.pos

            if player.health > 0:
                game_map[y][x] = '%d' % player.sid
            else:
                game_map[y][x] = '%d[dead]' % player.sid

    def _handle_request(self, socket, data):
        print 'server: in _handle_request'

        split_data = data.split(";");

        method_name = "handle_%s" % split_data[0].strip()

        if not hasattr(self, method_name):
            print "server: ERROR! got bad method_name: ", method_name
            return

        method = getattr(self, method_name)

        ret_val = None

        # ** login is a special case
        if method_name == 'handle_login':

            username, pass_hash = [s.strip() for s in split_data[1:]]

            sid = self.handle_login(socket, username, pass_hash)
            socket.sendall(str(sid))

        elif len(split_data) > 2:
            args = split_data[1:]
            ret_val = method(*args)

        elif len(split_data) > 1:
            args = split_data[1].strip()
            ret_val = method(args)
        else:
            ret_val = method()


        if ret_val:
            socket.sendall(str(ret_val))

    def handle_login(self, socket, username, pass_hash):
        print 'server: in handle login. %s, %s, %s' % (socket, username, pass_hash)
        stored_pass_hash = users.get(username)

        sid = sid_generator.next()

        if pass_hash == stored_pass_hash:
            sid_to_player_map[sid] = Player(sid)

        self._update_game_map()
        self.print_map()

        return sid


    def handle_logout(self, sid):
        sid = int(sid)
        print 'server: in handle logout. %s'% sid
        if sid in sid_to_player_map:
            del sid_to_player_map[sid]

    def handle_show_player(self, sid):
        sid = int(sid)
        player = sid_to_player_map.get(sid)
        return str(player)

    def handle_get_all_players(self, sid):
        sid = int(sid)
        if not sid in sid_to_player_map:
            return 'invalid session id'

        return [str(player) for player in sid_to_player_map.values]


    def handle_move(self, sid, relative_pos_str):
        sid = int(sid)
        print 'server: in handle move. %s, %s'% (sid, str(relative_pos_str))
        player = sid_to_player_map.get(sid)
        print 'server: player_map', sid_to_player_map

        if player == None:
            return 'invalid session id'

        relative_pos = eval(relative_pos_str)

        x, y = player.pos
        game_map[y][x] = ' '

        player.pos[0] += relative_pos[0]
        player.pos[1] += relative_pos[1]

        # make sure player isn't outside bounds
        player.pos[0] = min(max(player.pos[0], 0), xmax)
        player.pos[1] = min(max(player.pos[1], 0), ymax)

        x, y = player.pos

        game_cell = game_map[y][x]

        self._update_game_map()

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

        self.print_map()


    def handle_equip(self, sid, weapon_name):
        sid = int(sid)
        weapon_name = weapon_name.strip()
        print 'server: in handle equip. %s, %s'% (sid, weapon_name)

        player = sid_to_player_map.get(sid)
        if player == None:
            return 'invalid session id'

        player.try_equip(weapon_name)

        print str(player)


    def handle_attack(self, sid, target_id):
        print 'server: in handle attack. %s, %s'% (sid, target_id)

        sid = int(sid)
        target_id = int(target_id)

        player = sid_to_player_map.get(sid)
        if player == None:
            return 'invalid session id'

        target = sid_to_player_map.get(target_id)
        if target:
            player.attack(target)

        self._update_game_map()

        print str(player)


    def handle_use_potion(self, sid, potion_name):
        sid = int(sid)
        print 'server: in handle_use_potion. %s, %s'%  (sid, potion_name)
        player = sid_to_player_map.get(sid)
        if player == None:
            return 'invalid session id'

        player.use_potion(potion_name)

        print str(player)


    def handle_show_map(self, sid):
        sid = int(sid)
        print 'server: in handle_show_map. %s'% (sid)

        player = sid_to_player_map.get(sid)
        if player == None:
            return 'invalid session id'

        #TODO: make this work

        return game_map

    def check_request_interval(self, sock):

        if not constants.CHECK_REQUEST_INTERVAL:
            return False

        prev_time = sock_to_request_time.setdefault(sock, 0)
        cur_time = time.time()
        delta_time = cur_time - prev_time

        print 'prev_time: ', prev_time   
        print 'cur_time: ', cur_time  
        print 'delta_time: ', delta_time 

        invalid_interval = prev_time != 0 and delta_time < constants.MIN_REQUEST_INTERVAL


        if invalid_interval: 
            return False

        sock_to_request_time[sock] = cur_time

        return True

    def detect_bots(self, sock):

        request_interval_valid = self.check_request_interval(sock)

        if request_interval_valid:
            return False
        else:
            return True

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
                    connected_socket = ssl.wrap_socket(connected_socket,
                                                       server_side=True,
                                                       certfile='cert.pem',
                                                       keyfile='cert.pem',
                                                       ssl_version=ssl.PROTOCOL_TLSv1)

                    print 'server: got connection from ', client_address

                    sid = connected_socket.getpeername()
                    sock_list.append(connected_socket)

                #if there's data coming in (another socket's state changed)
                else:
            #        try:
                    data = sock.recv(constants.BUFFER_SIZE)

                    bot_detected = self.detect_bots(sock)

                    if bot_detected:
                        print 'server: BOT DETECTED! Ignoring request.'
                        return

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

    def print_map(self):
        #os.system('clear')
        print '\n'.join([str(row) for row in game_map])


