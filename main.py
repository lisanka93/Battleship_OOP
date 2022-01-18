from helper import *
from data import game_data


if __name__ == "__main__":
    """
    Prints battleship info and rules
    Instantiates two player objects. If is_computer=True, that player will act as a computer
    Plays battleship between the two players with ships in data.json
    """
    print_battleship_info()

    player = Player(name=input(f"Your name: "), is_computer=False)
    computer = Player(name="Computer", is_computer=True)
    data = game_data

    play_battleship(player, computer, data)
