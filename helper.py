from player import Player

def play_battleship(player_1, player_2, game_data):
    """
    Builds each player's grid and ships. Both players print their grids and attack each other until a player has no ships left
    """
    player_1.build_grid(game_data)
    player_2.build_grid(game_data)

    while True:
        player_2.print_grid()
        player_1.print_grid()
        player_1.attack(player_2.grid)
        player_2.attack(player_1.grid)

def print_battleship_info():
    print(
    """
    Welcome to Battleship!

    In this game you will play against the computer and you each try to sink each other's ships.
    (Note: The ships will be randomply placed on the board for you)
    The player who first sinks all the opponent's ships wins!

    Grid coordinates are given in the following format: letter followed by number (e.g. B6)

    If you would like to automate the entire game, pass 'is_computer=True' to both player objects in play_battelship.py
""")
