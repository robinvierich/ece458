import socket
import threading
import select

import constants
from player import Player
from models import User, Item, Resource

#{ session id : player }
sid_to_player_map = {}


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

    def _handle_request(self, data):
        split_data = data.split(",");
        if (len(split_data) > 1):
            eval("self.handle_%s(*split_data[1:])" % split_data[0].strip())
        else:
            eval("self.handle_%s()" % split_data[0].strip())


    def handle_login(self, username, pass_hash):
        print 'server: in handle login. %s, %s' % (username, pass_hash)
        pass

    def handle_logout(self, sid):
        print 'server: in handle logout'% (sid)


    def handle_move(self, sid, relative_pos):
        print 'server: in handle move'% (sid, relative_pos)
        pass


    def handle_equip(self, sid, item):
        print 'server: in handle equip'% (sid, item)
        pass


    def handle_attack(self, sid, item):
        print 'server: in handle attack'% (sid, item)
        pass


    def handle_gather(self, sid, resource):
        print 'server: in handle gather'%  (sid, resource)
        pass


    def handle_buy(self, sid, item):
        print 'server: in handle buy' % (sid, item)
        pass


    def handle_sell(self, sid, item):
        print 'server: in handle sell' % (sid, item)
        pass


    def handle_get_visible_player_positions(self, sid):
        print 'server: in handle get_visible_player_positions'% (sid)
        pass


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
                    sid_to_player_map.setdefault(sid, Player(sid))
                    sock_list.append(connected_socket)

                #if there's data coming in (another socket's state changed)
                else:
                    try:
                        data = sock.recv(constants.BUFFER_SIZE)
                        real_sid = sock.getpeername()

                        if data:
                            print 'server: received data from ', client_address
                            print 'server: data = ', data
                            self._handle_request(sid, data)
                        else:
                            print 'server: no more data from ', client_address
                            sock.close()
                            sock_list.remove(sock)
                            break

                    except e as Exception:
                        print 'server: Connection ERROR! ', e
                        sock.close()

    def stop(self):
        print 'server: stopping server thread'
        self._running = False
        print 'server: joining server thread'
        self.join()
        print 'server: server thread joined'


