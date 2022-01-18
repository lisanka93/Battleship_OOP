class Ship:
    """
    A Ship has a name, and health, and a list of coordinates
    """
    def __init__(self, name="default", health=0, coords=0):

        self.name = str(name)
        self.health = int(health)
        self.coords = coords

    def get_name(self):
        return self.name

    def get_coords(self):
        return self.coords

    def set_coords(self, coords):
        self.coords = coords

    def decrement_health(self):
        self.health -= 1
        if self.health == 0:
            print(f"You sunk my {self.name}!")
