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

    client_commands = []
    for attr_name in dir(client):
        attr = getattr(client, attr_name)

        if callable(attr) and not attr_name.startswith('__'):

            args = [arg for arg in inspect.getargspec(attr)[0] if not arg == 'self']
            client_commands.append("%s %s" % (attr_name, ' '.join(args)))

    return ['help', 'quit'] + client_commands

def handle_command(command):
    print 'got command ', command
    if command == 'help':
        command_list = get_command_list()

        command_list_str = '\n'.join(command_list).replace('\'', '').replace('[','').replace(']','')

        return '\n' + command_list_str + '\n'

    if command == 'quit':
        server.stop()
        quit()

    split_command = command.split(' ')
    command_name = split_command[0].strip()

    print split_command

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


