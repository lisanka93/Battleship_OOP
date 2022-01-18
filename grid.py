from ship import Ship
import random



class Grid:
    """
    A Grid has rows and columns, a list of ships, a list of ship locations, and a dictionary of previous moves
    """

    def __init__(self, rows=0, cols=0):

        self.rows = int(rows)
        self.cols = int(cols)
        self.grid_ships = []
        self.ship_locations = []
        self.available_locations = []    #needed to initialise with space in between ships
        self.shots_dict = {}


    def build_ships(self, ship_data):
        for ship in ship_data:
            self.grid_ships.append(Ship(name=ship["name"], health=ship["health"]))


    def set_available_locations(self):

        """
        stores all available locations - these are needed to track which locations are gone
        once a ship was placed there to delete all surrounding fields from available locations
        """

        for i in range(self.rows):
            for j in range(self.cols):
                self.available_locations.append((i,j))

    def build_ship_coordinates(self, ship):

        """
        builds the coordinates for each ship taken the constraint into accound that between all
        ships there needs to be at least one spare square
        """
        # Randomly choose a coordinate on the grid, and randomly choose orientation
        found = False

        while found == False:

            test = random.choice(self.available_locations)

            row = test[0]
            col = test[1]

            vertical = random.choice([True, False])

            possible_coordinates = []

            if vertical == True:
                for i in range(ship.health):
                    possible_coordinates.append((row,col))
                    row += 1
            else:
                for i in range(ship.health):
                    possible_coordinates.append((row,col))
                    col += 1

            if set(possible_coordinates).issubset(self.available_locations):
                self.available_locations = [x for x in self.available_locations if x not in possible_coordinates]
                found = True
                #print("available locations", self.available_locations)
                #print("coordinates chosen", possible_coordinates)

                if vertical == True:
                    to_delete = [(possible_coordinates[0][0]-1, possible_coordinates[0][1]),
                                (possible_coordinates[-1][0]+1,possible_coordinates[-1][1]),
                                (possible_coordinates[0][0]-1, possible_coordinates[0][1]-1),
                                (possible_coordinates[0][0]-1, possible_coordinates[0][1]+1),
                                (possible_coordinates[-1][0]+1, possible_coordinates[-1][1]-1),
                                (possible_coordinates[-1][0]+1, possible_coordinates[-1][1]+1)]
                    for c in possible_coordinates:
                        to_delete.extend(((c[0],c[1]-1),(c[0],c[1]+1)))

                else:
                    to_delete = [(possible_coordinates[0][0], possible_coordinates[0][1]-1),
                                (possible_coordinates[-1][0],possible_coordinates[-1][1]+1),
                                (possible_coordinates[0][0]-1, possible_coordinates[0][1]-1),
                                (possible_coordinates[0][0]+1, possible_coordinates[0][1]-1),
                                (possible_coordinates[-1][0]-1, possible_coordinates[-1][1]+1),
                                (possible_coordinates[-1][0]+1, possible_coordinates[-1][1]+1)]
                    for c in possible_coordinates:
                        to_delete.extend(((c[0]-1,c[1]),(c[0]+1,c[1])))

                self.available_locations = [x for x in self.available_locations if x not in to_delete]

        return possible_coordinates

    def randomly_set_ship_locations(self):

        """
        it is very likely to happen that available space will run out due to the small grid
        and the restriction of having a space in between each ship. so we need to try many
        times to initialise the grid
        """

        worked = False
        while worked==False:

            try:
                self.set_available_locations()

                for ship in self.grid_ships:
                    ship_coords = self.build_ship_coordinates(ship)

                    # Set this ship's coords, and add them to ship locations
                    ship.set_coords(ship_coords)

                    for coord in ship_coords:
                        self.ship_locations.append(coord)

                    #if len(self.ship_locations) == 11:
                        #worked=True
            except:
                self.ship_locations=[]
                pass
            else:
                #print(self.ship_locations)
                worked=True




    def attack_not_in_shots_dict(self, coord, col, row, is_computer):
        """
        checking whether player did not attack the same cell before
        """

        if str(col)+str(row) not in self.shots_dict:
            return True
        # Let player know they already shot here
        if not is_computer:
            print(f"{coord} has already been shot.")
        return False

    def attack_inside_grid(self, coord, col, row):
        if col in range(self.cols) and row in range(self.rows):
            return True
        print(f"{coord} is outside the grid bounds.")
        return False


    def all_ships_sunk(self):
        # If a ship has health > 0, not all ships are sunk
        for ship in self.grid_ships:
            if ship.health > 0:
                return False
        return True
