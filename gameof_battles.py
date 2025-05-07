def parse_position(pos):
    row = ord(pos[0].upper()) - ord("A")
    col = int(pos[1:]) - 1
    return row, col

#Ship class
class Ship:
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = []
    def place(self,start,direction):
        row, col = start
        self.positions = []
        for i in range(self.size):
            if direction == "H":
                self.positions.append((row, col + i))
            else:
                self.positions.append((row + i, col))

    def is_sunk(self):
        return all(pos in self.hits for pos in self.positions)
    def register_hit(self,pos):
        if pos in self.positions and pos not in self.hits:
            self.hits.append(pos)

#Board class
class Board:
    def __init__(self):
        self.grid = [["-"] * 10 for _ in range(10)]
        self.ships = []

    def place_ship(self,ship,start,direction):
        ship.place(start,direction)

        for r, c in ship.positions:
            if not (0 <= r < 10 and 0 <= c < 10):
                print("Ship is going out of board try again")
                return False

        for existing in self.ships:
            if set(ship.positions) & set(existing.positions):
                print("Ships overlapping try again")
                return False

        self.ships.append(ship)
        for r,c in ship.positions:
            self.grid[r][c] = "S"
        return True

    def receive_attack(self,row,col):
        for ship in self.ships:
            if (row,col) in ship.positions:
                if(row,col) in ship.hits:
                    return "Alredy Hit"
                ship.register_hit((row, col))
                self.grid[row][col] = "X"
                if ship.is_sunk():
                    return  f"Sunk {ship.name}"
                return "Hit"
        self.grid[row][col] = "0"
        return "Miss"

    def print_board(self, show_ships=False):
        print("   " + " ".join([str(i + 1).rjust(2) for i in range(10)]))
        for xyz, row in enumerate(self.grid):
            row_label = chr(ord("A") + xyz)
            display_row = []
            for cell in row:
                if cell == "S" and not show_ships:
                    display_row.append("~")
                else:
                    display_row.append(cell)
            print(row_label + "  " + " ".join(display_row))

#Player Class
class Player:
    def __init__(self,name):
        self.name = name
        self.own_board = Board()
        self.tracking_board = Board()

    def ship_placing(self):
        ship_types = [("Carrier", 5),("Battleship", 4),("Cruiser", 3),("Submarine", 3),("Destroyer", 2)]

        print(f"\n{self.name}, place your ships:")
        for name, size in ship_types:
            placed = False
            while not placed:
                try:
                    print(f"\nPlacing {name} (size {size})")
                    pos = input("Enter start position (e.g., A3): ").strip().upper()
                    direction = input("Enter direction (H for horizontal, V for vertical): ").strip().upper()
                    row, col = parse_position(pos)
                    ship = Ship(name, size)
                    placed = self.own_board.place_ship(ship, (row, col), direction)
                except Exception as e:
                    print(f"Invalid input: {e}")

    def take_turn(self, opponent):
        while True:
            command = input(f"\n{self.name}'s turn (e.g., Fire C5 or Draw Board): ").strip().upper()

            if command.startswith("FIRE"):
                try:
                    _, pos = command.split()
                    row, col = parse_position(pos)
                    result = opponent.own_board.receive_attack(row, col)

                    if result.startswith("Hit") or result.startswith("Sunk"):
                        self.tracking_board.grid[row][col] = "X"
                    elif result == "Miss":
                        self.tracking_board.grid[row][col] = "O"

                    print(f"{self.name} fires at {pos}: {result}")
                    break
                except Exception as e:
                    print(f"Invalid fire command: {e}")
            elif command == "DRAW BOARD":
                print("\nYour Ships:")
                self.own_board.print_board(show_ships=True)
                print("\nYour Hits/Misses:")
                self.tracking_board.print_board()
            else:
                print("Invalid command. Try again.")

#Game Class
class Game:
    def __init__(self,n1,n2):
        self.p1 = Player(n1)
        self.p2 = Player(n2)
        self.cp = self.p1
        self.opponent = self.p2

    def switch(self):
        self.cp,self.opponent = self.opponent,self.cp

    def game_over(self):
        return all(ship.is_sunk() for ship in self.opponent.own_board.ships)

    def start(self):
        print("   Welcome to BattleShip   ")
        self.p1.ship_placing()
        self.p2.ship_placing()

        while True:
            self.cp.take_turn(self.opponent)

            if self.game_over():
                print(f" {self.cp.name} wins. \n Enemy has been defeated.")
                break
            self.switch()

if __name__ == "__main__":
    print(" *** BATTLESHIP GAME *** ")
    name1 = input("Enter name of player 1: ")
    name2 = input("Enter name of player 2: ")
    game = Game(name1,name2)
    game.start()