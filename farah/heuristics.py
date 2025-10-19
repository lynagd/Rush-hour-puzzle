from rush_hour_puzzle import RushHourPuzzle

def h1_distance_to_exit(state: RushHourPuzzle) -> int:
    #Heuristic 1: Distance from red car to exit.

    # Find the red car
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            # Current position of red car
            current_x = vehicle['x']
            
            # Target position (exit)
            target_x = state.board_width - 2
            
            # Distance to travel (only horizontal for red car)
            distance = target_x - current_x
            
            return max(0, distance)  # Return 0 if already at or past exit
    
    return 0  # Should never happen if X exists


def h2_blocking_vehicles(state: RushHourPuzzle) -> int:
   
    #Heuristic 2: h1 + number of vehicles blocking the path to exit.

    # Start with h1 (distance to exit)
    h1 = h1_distance_to_exit(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if red_car is None:
        return h1
    
    # Red car's row (the exit row)
    red_y = red_car['y']
    
    # Red car's rightmost position
    red_right = red_car['x'] + red_car['length']
    
    # Exit position
    target_x = state.board_width - 2
    
    # Count unique blocking vehicles
    blocking_vehicles = set()
    
    # Check each position from red car to exit
    for x in range(red_right, target_x + 1):
        # Check if position is within board
        if x < state.board_width:
            cell = state.board[red_y][x]
            # If there's a vehicle (not empty and not X itself)
            if cell != '.' and cell != 'X' and cell != '#':
                blocking_vehicles.add(cell)
    
    # Return distance + number of blocking vehicles
    return h1 + len(blocking_vehicles)


def h3_advanced_heuristic(state: RushHourPuzzle) -> int:
    """
    Heuristic 3: Advanced heuristic considering blocking vehicles 
    and their mobility constraints.
    
    This heuristic considers:
    1. Distance to exit (h1)
    2. Number of blocking vehicles (from h2)
    3. Mobility penalty: How "stuck" each blocking vehicle is
    4. Secondary blockers: Vehicles blocking the blocking vehicles
    
    The idea: If a vehicle blocks the red car, and that vehicle itself
    is blocked, we need more moves to free the path.
    """
    # Start with h2
    h2 = h2_blocking_vehicles(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if red_car is None:
        return h2
    
    red_y = red_car['y']
    red_right = red_car['x'] + red_car['length']
    target_x = state.board_width - 2
    
    # Find all vehicles directly blocking the red car
    blocking_vehicle_ids = set()
    for x in range(red_right, target_x + 1):
        if x < state.board_width:
            cell = state.board[red_y][x]
            if cell != '.' and cell != 'X' and cell != '#':
                blocking_vehicle_ids.add(cell)
    
    # Calculate mobility penalty for each blocker
    penalty = 0
    
    for blocking_id in blocking_vehicle_ids:
        # Find this vehicle's info
        blocking_vehicle = None
        for vehicle in state.vehicles:
            if vehicle['id'] == blocking_id:
                blocking_vehicle = vehicle
                break
        
        if blocking_vehicle is None:
            continue
        
        # Check mobility of this blocking vehicle
        orientation = blocking_vehicle['orientation']
        x = blocking_vehicle['x']
        y = blocking_vehicle['y']
        length = blocking_vehicle['length']
        
        if orientation == 'V':  # Vertical vehicle blocking horizontal path
            # Check if it can move up
            can_move_up = y > 0 and state.board[y - 1][x] == '.'
            
            # Check if it can move down
            can_move_down = (y + length < state.board_height and 
                            state.board[y + length][x] == '.')
            
            # Penalty based on mobility
            if not can_move_up and not can_move_down:
                # Completely stuck - high penalty
                penalty += 3
                
                # Count secondary blockers
                if y > 0:
                    cell_above = state.board[y - 1][x]
                    if cell_above != '.' and cell_above != '#':
                        penalty += 1  # Something blocks movement up
                
                if y + length < state.board_height:
                    cell_below = state.board[y + length][x]
                    if cell_below != '.' and cell_below != '#':
                        penalty += 1  # Something blocks movement down
            
            elif not can_move_up or not can_move_down:
                # Can only move in one direction - moderate penalty
                penalty += 1
        
        elif orientation == 'H':  # Horizontal vehicle in the path
            # Check if it can move left
            can_move_left = x > 0 and state.board[y][x - 1] == '.'
            
            # Check if it can move right
            can_move_right = (x + length < state.board_width and 
                             state.board[y][x + length] == '.')
            
            # Penalty based on mobility
            if not can_move_left and not can_move_right:
                # Completely stuck
                penalty += 3
            elif not can_move_left or not can_move_right:
                # Limited mobility
                penalty += 1
    
    return h2 + penalty


# Optional: Alternative h3 that's simpler but still effective
def h3_simple_penalty(state: RushHourPuzzle) -> int:
    """
    Alternative Heuristic 3: Simpler version with fixed penalties.
    
    """
    h2 = h2_blocking_vehicles(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if red_car is None:
        return h2
    
    red_y = red_car['y']
    red_right = red_car['x'] + red_car['length']
    target_x = state.board_width - 2
    
    # Find blocking vehicles
    blocking_vehicle_ids = set()
    for x in range(red_right, target_x + 1):
        if x < state.board_width:
            cell = state.board[red_y][x]
            if cell != '.' and cell != 'X' and cell != '#':
                blocking_vehicle_ids.add(cell)
    
    # Simple penalty: add 2 for each blocker (assumes they need clearing)
    penalty = len(blocking_vehicle_ids) * 2
    
    return h2 + penalty