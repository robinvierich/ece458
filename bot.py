from client import Client
from server import Server

#dummy_server = Server()
#dummy_server.start()

client = Client()

username = 'admin'
pass_hash = 'admin'


sid = client.login(username, pass_hash)

def get_player_position():
    game_map = client.show_map()

    for i, row in enumerate(game_map):
        for j, col in enumerate(row):
            if game_map[i][j] == str(client._sid):
                return [j, i] # j is x-pos, i is y-pos


def print_map(game_map):
    print '\n'
    print '\n'.join([str(row) for row in game_map])
    print '\n'


def collect_all_items():
    game_map = client.show_map()

    for i, row in enumerate(game_map):
        for j, col in enumerate(row):
            if col != ' ' and col != 'x':
                x, y = get_player_position()
                move_vect = [j - x, i - y]
                client.move(move_vect)
                game_map = client.show_map()
                print_map(game_map)


def attack_players():
    # TODO hardcoded this for now, need to search through
    # players's items and find the one with biggest damage
    client.equip('staff')

    game_map = client.show_map()

    for i, row in enumerate(game_map):
        for j, col in enumerate(row):

            try:
                enemy_id = int(col)
            except ValueError: # if cast fails
                continue

            if enemy_id == client._sid:
                continue

            client.attack(enemy_id)

            game_map = client.show_map()
            print_map(game_map)



def play_game():
    collect_all_resources()
    attack_players()


collect_all_items()

print 'BOT: collect all items done'

player_str = client.show_player()

print 'BOT: player ', player_str

attack_players()

print 'BOT: DONE'
#dummy_server.stop()
quit()

