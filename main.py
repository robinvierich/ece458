import inspect

from server import Server
from client import Client


server = Server()
server.start()


client = Client()

print 'starting test'
print 'enter "help" for list of commands'

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
        return "\n".join(get_command_list())

    if command == 'quit':
        server.stop()
        quit()

    split_command = command.split(' ')
    command_name = split_command[0]

    if len(split_command) > 1:
        args = split_command[1:]
    else:
        args = []

    method = getattr(client, command_name)
    if not method:
        return None

    return method(*args)


while True:
    print handle_command(raw_input('Enter command: '))


