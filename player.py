from grid import Grid
import random

class Player:

    def __init__(self, name="default", grid=None, is_computer=False):
        self.name = str(name)
        self.grid = grid
        self.is_computer = is_computer


    @staticmethod
    def validate_data_get_dimensions(game_data):
        """
        Checks rows * cols < sum_ship_health*2+2 (assuming optimal initialisation)
        Checks rows and cols < max_ship_health
        Returns the dimensions and ships data
        """

        dimensions = game_data[0]
        rows = dimensions["rows"]
        cols = dimensions["cols"]

        ships = game_data[1:]

        max_ship_health = 0
        space_needed = 0   #space needed on grid

        for ship in ships:
            space_needed += ship["health"]*2+2
            if ship["health"] > max_ship_health:
                max_ship_name = ship["name"]
                max_ship_health = ship["health"]

        if rows * cols  < space_needed:
                print("Grid dimensions not large enough to place all ships. Please increase grid size. Exiting.")
                exit(1)

            # Check rows and cols < max ship["health"]
        if rows < max_ship_health and cols < max_ship_health:
                print(f"Grid dimensions not large enough for {max_ship_name}. Please increase grid size. Exiting.")
                exit(1)

        return dimensions, ships

    def build_grid(self, game_data):
        """
        Validates the data and build the grid including the ships
        """

        dimensions, ships = self.validate_data_get_dimensions(game_data)

        self.grid = Grid(rows=dimensions["rows"], cols=dimensions["cols"])
        self.grid.build_ships(ships)
        self.grid.randomly_set_ship_locations()

    def get_and_validate_player_input(self):
        """
        Checks user input is within grid. Assumes the grid has equal cols and rows
        """

        while True:
            coord = input("Choose a coordinate to fire on: ").lower()
            print()
            if 1 < len(coord) <= len(str(self.grid.cols)) + 1:
                break
            print("Bad length. Coordinate must be of the form a10 or J1")
        return coord


    def get_attack_coord(self, enemy_grid):
        #generating random valid move for computer
        if self.is_computer:
            coord = chr(random.randrange(97, 97 + enemy_grid.cols)) + str(random.randint(1, enemy_grid.rows))
        else:
            coord = self.get_and_validate_player_input()
        return coord


    def validate_and_get_attack_coord(self, enemy_grid):
            while True:
                coord = self.get_attack_coord(enemy_grid)
                try:
                    #check whether throws error - if not ignore and handle as out of bound error
                    col, row = int(ord(coord[0])) - 97, int(coord[1:]) - 1
                    print("col ", col, "row ", row)
                except ValueError:
                    "Bad Input. Coordinate must be of the form a10 or J1"
                else:
                    not_in_shots_dict = enemy_grid.attack_not_in_shots_dict(coord, col, row, self.is_computer)
                    in_grid = enemy_grid.attack_inside_grid(coord, col, row)

                    if not_in_shots_dict and in_grid:
                        break
            return coord, col, row

    def damage_ship_and_get_location_data(self, coord, col, row, enemy_grid):
        """
        Sets default location_data to a miss. If the (col, row) is a ship location,
        mark it has a hit, and decrement ship health. Then, check if the game is over
        """
        location_data = "O"
        if (row, col) in enemy_grid.ship_locations:
            location_data = "X"
            print(f"{coord} was a hit!")
            print()

            # Find the ship that was hit, and decrement it's health. Check if game is over
            for ship in enemy_grid.grid_ships:
                if (row, col) in ship.get_coords():
                    ship.decrement_health()
                    self.is_game_over(enemy_grid)

        if location_data == "O":
            print(f"{coord} missed!")
            print()
        return location_data

    def is_game_over(self, enemy_grid):
        if enemy_grid.all_ships_sunk():
            print(f"{self.name} wins!")
            exit(0)

    def attack(self, enemy_grid):
        coord, col, row = self.validate_and_get_attack_coord(enemy_grid)
        print(f"{self.name} attacked {coord}!")
        print()

        location_data = self.damage_ship_and_get_location_data(coord, col, row, enemy_grid)

        # Update the location data to the shots dictionary
        enemy_grid.shots_dict[str(col) + str(row)] = location_data


    def print_grid(self):


        print(self.name)
        # Print offset, and col headers, considering num rows could change
        print(' ' * (len(str(self.grid.rows)) + 1), end="")
        print(*[chr(c+97).upper() for c in range(self.grid.cols)], end="")


        for r in range(self.grid.rows):
            # Print row headers, and offset considering num rows could change
            offset = ' ' * ((len(str(self.grid.rows))) - len(str(r+1)))
            print(f"\n{r+1} " + offset, end="")

            for c in range(self.grid.cols):
                coord = str(c)+str(r)
                location_info = self.grid.shots_dict.get(coord, "~")
                #print("ingo",location_info)

                # If not computer grid, we should print our ship
                if coord not in self.grid.shots_dict and (r, c) in self.grid.ship_locations and not self.is_computer:
                    for ship in self.grid.grid_ships:
                        if (r,c) in ship.get_coords():
                            location_info = "■"

                print(location_info + " ", end="")
        print("\n")
        #"""
