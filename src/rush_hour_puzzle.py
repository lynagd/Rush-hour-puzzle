import csv
import copy

class RushHourPuzzle:
   # Initialize the puzzle state
    
    def __init__(self, csv_file=None, vehicles=None, board_height=6, board_width=6):
       
        self.board_height = board_height
        self.board_width = board_width
        self.vehicles = []  
        self.walls = []    
        self.board = []     
        
        if csv_file:
            # open the CSV file in read mode (if provided)
            self.setVehicles(csv_file)
        elif vehicles:
            # set the vehicles list
            self.vehicles = vehicles
        
        # Create the board visualization
        self.setBoard()
    
    def setVehicles(self, csv_file):
        # Read and create vehicles and walls from a CSV file
        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                
                # Read first line for board dimensions
                first_line = next(reader)
                self.board_height = int(first_line[0])
                self.board_width = int(first_line[1])
                
                # Read vehicles and walls
                for row in reader:
                    if row[0] == '#':
                        # It's a wall
                        wall_x = int(row[1])
                        wall_y = int(row[2])
                        self.walls.append((wall_x, wall_y))
                    else:
                        # It's a vehicle: id, x, y, orientation, length
                        vehicle = {
                            'id': row[0],
                            'x': int(row[1]),
                            'y': int(row[2]),
                            'orientation': row[3],  # 'H' or 'V'
                            'length': int(row[4])
                        }
                        self.vehicles.append(vehicle)
        
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found!")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
    
    def setBoard(self):
        
        # Initialize empty board with '.' characters
        self.board = [['.' for _ in range(self.board_width)] 
                      for _ in range(self.board_height)]
        
        # Place walls on the board
        for wall_x, wall_y in self.walls:
            self.board[wall_y][wall_x] = '#'
        
        # Place vehicles on the board
        for vehicle in self.vehicles:
            vid = vehicle['id']
            x = vehicle['x']
            y = vehicle['y']
            orientation = vehicle['orientation']
            length = vehicle['length']
            
            # Place vehicle squares on board
            if orientation == 'H':  # Horizontal
                for i in range(length):
                    self.board[y][x + i] = vid
            else:  # Vertical
                for i in range(length):
                    self.board[y + i][x] = vid
    
    def isGoal(self):
        # Find the red car 'X'
        for vehicle in self.vehicles:
            # middle right is the exit position
            if vehicle['id'] == 'X':
                target_x = self.board_width - 2
                target_y = self.board_height // 2 - 1
                
                # Check if X car is at the exit position
                return vehicle['x'] == target_x and vehicle['y'] == target_y
        
        return False
    
    def successorFunction(self):
       # Generate all possible successor states from the current state
        successors = []
        
        # Try moving each vehicle
        for i, vehicle in enumerate(self.vehicles):
            vid = vehicle['id']
            x = vehicle['x']
            y = vehicle['y']
            orientation = vehicle['orientation']
            length = vehicle['length']
            
            if orientation == 'H':
                
                # Try moving LEFT
                if x > 0 and self.board[y][x - 1] == '.':
                    # Create new vehicle list with updated position
                    new_vehicles = copy.deepcopy(self.vehicles)
                    new_vehicles[i]['x'] = x - 1
                    
                    # Create successor state
                    successor_state = RushHourPuzzle(
                        vehicles=new_vehicles,
                        board_height=self.board_height,
                        board_width=self.board_width
                    )
                    # Copy the walls into the new state
                    successor_state.walls = copy.deepcopy(self.walls)
                    # Rebuild the board with the walls included
<<<<<<< HEAD
                    successor_state.setBoard()                    
=======
                    successor_state.setBoard()
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
                    successors.append(((vid, 'L'), successor_state))
                
                # Try moving RIGHT
                if x + length < self.board_width and self.board[y][x + length] == '.':
                    new_vehicles = copy.deepcopy(self.vehicles)
                    new_vehicles[i]['x'] = x + 1
                    
                    successor_state = RushHourPuzzle(
                        vehicles=new_vehicles,
                        board_height=self.board_height,
                        board_width=self.board_width
                    )
                    # Copy the walls into the new state
                    successor_state.walls = copy.deepcopy(self.walls)
                    # Rebuild the board with the walls included
<<<<<<< HEAD
                    successor_state.setBoard()                    
=======
                    successor_state.setBoard()

>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
                    successors.append(((vid, 'R'), successor_state))
            
            else:  # Vertical vehicle
               
                # Try moving UP
                if y > 0 and self.board[y - 1][x] == '.':
                    new_vehicles = copy.deepcopy(self.vehicles)
                    new_vehicles[i]['y'] = y - 1
                    
                    successor_state = RushHourPuzzle(
                        vehicles=new_vehicles,
                        board_height=self.board_height,
                        board_width=self.board_width
                    )
                    # Copy the walls into the new state
                    successor_state.walls = copy.deepcopy(self.walls)
                    # Rebuild the board with the walls included
<<<<<<< HEAD
                    successor_state.setBoard()                    
=======
                    successor_state.setBoard()

>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
                    successors.append(((vid, 'U'), successor_state))
                
                # Try moving DOWN
                if y + length < self.board_height and self.board[y + length][x] == '.':
                    new_vehicles = copy.deepcopy(self.vehicles)
                    new_vehicles[i]['y'] = y + 1
                    
                    successor_state = RushHourPuzzle(
                        vehicles=new_vehicles,
                        board_height=self.board_height,
                        board_width=self.board_width
                    )
                    # Copy the walls into the new state
                    successor_state.walls = copy.deepcopy(self.walls)
                    # Rebuild the board with the walls included
<<<<<<< HEAD
                    successor_state.setBoard()                    
=======
                    successor_state.setBoard()
                    
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
                    successors.append(((vid, 'D'), successor_state))
        
        return successors
    
    def __eq__(self, other):
        # Checks duplicate states
        if not isinstance(other, RushHourPuzzle):
            return False
        
        # Compare vehicle positions
        for v1, v2 in zip(self.vehicles, other.vehicles):
            if v1['x'] != v2['x'] or v1['y'] != v2['y']:
                return False
        
        return True
    
    def __hash__(self):
        """
        Create a hash for the state (needed for set/dict operations).
        """
        # Create a tuple of vehicle positions for hashing
        positions = tuple((v['id'], v['x'], v['y']) for v in sorted(self.vehicles, key=lambda v: v['id']))
        return hash(positions)
    
    def __str__(self):
        # String representation of the board
        result = ""
        for row in self.board:
            result += " ".join(row) + "\n"
        return result