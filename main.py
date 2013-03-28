import inspect
import time

from server import Server
from client import Client


server = Server()
server.start()


client = Client()

print 'starting test'

def get_command_list():
    # get all methods on the client class
    client_commands = [
            "%s(%s)" % (attr, str(inspect.getargspec(getattr(client, attr))[0]))
            for attr in dir(client) 
            if callable(getattr(client, attr)) and not attr.startswith('__') 
    ]

    return ['help', 'quit'] + client_commands

def handle_command(command):
    print 'got command ', command
    if command == 'help':
        return '\n' + '\n'.join(get_command_list()) + '\n'

    if command == 'quit':
        server.stop()
        quit()

    split_command = command.split(' ')
    command_name = split_command[0]

    if len(split_command) > 1:
        args = split_command[1:]
    else:
        args = []

    if not hasattr(client, command_name):
        return None

    method = getattr(client, command_name)
    return method(*args)


while True:
    time.sleep(0.1)
    print 'Enter "help" for list of commands'
    print 'Enter command: ', handle_command(raw_input())


