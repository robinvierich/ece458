import socket
import threading
import select

import constants

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

    def run(self):
        print 'server: server thread started'

        self._running = True

        sock_list = [self._sock]

        while self._running:
            try:
                readable_socks, writable_socks, err_socks = select.select(sock_list, [], [], 1.0)
            except socket.timeout as e:
                print 'got timeout ', e
                continue

            for sock in readable_socks:

                # if there's a new connection coming in (self._sock state changed)
                if sock is self._sock:
                    connected_socket, client_address = self._sock.accept() # blocks waiting for connection
                    print 'server: got connection from ', client_address

                    sock_list.append(connected_socket)

                #if there's data coming in (another socket's state changed)
                else:
                    try:
                        data = sock.recv(constants.BUFFER_SIZE)

                        if data:
                            print 'server: received data from ', client_address
                            print 'server: data = ', data
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


