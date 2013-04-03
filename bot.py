from client import Client

client = Client()

username = 'admin'
pass_hash = 'admin'


sid = client.login(username, pass_hash)

def get_player_position():
    game_map = client.get_visible_map()

    for i, row in enumerate(game_map):
        for j, col in enumerate(row):
            if game_map[i][j] == 'x':
                return [j, i] # j is x-pos, i is y-pos


def collect_all_items():
    x, y = get_player_position()

    game_map = client.get_visible_map()

    relative_moves = []

    for i, row in enumerate(game_map):
        for j, col in enumerate(row):

            if col != ' ' and col != 'x':
                relative_moves.append([i - x, j - x])

    for vect in relative_moves:
        client.move(vect)

def print_map(game_map):
    '\n'.join([str(row) for row in game_map])

def attack_players():
    pass


def play_game():
    collect_all_resources()
    attack_players()



