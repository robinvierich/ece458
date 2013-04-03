from client import Client

client = Client()

username = 'admin'
pass_hash = 'admin'


sid = client.login(username, pass_hash)

def collect_all_items():
    #TODO: Get player position from server
    x, y = 0, 0 # current player position

    game_map = client.get_visible_map()

    relative_moves = []

    for i, row in enumerate(game_map):
        for j, col in enumerate(row):

            if col != ' ' and col != 'x':
                relative_moves.append([i - x, j - x])

    for vect in relative_moves:
        client.move(vect)


def attack_players():
    pass

def play_game():
    collect_all_resources()
    attack_players()


