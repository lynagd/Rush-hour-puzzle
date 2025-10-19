from collections import deque
import heapq
from node import Node


def BFS(initial_state):
    """
    Breadth-First Search algorithm following the course pseudocode (Figure 1.19).
    Explores the shallowest nodes first using a FIFO queue.
    
    Parameters:
    - initial_state: RushHourPuzzle instance representing the starting configuration
    
    Returns:
    - goal_node: Node containing the goal state, or None if no solution
    - steps: Number of nodes expanded
    """
    # Open: queue (FIFO list)
    open_list = deque()
    
    # Closed: list (using set for O(1) lookup)
    closed_set = set()
    
    # init_node <- Node (s, None, None)
    init_node = Node(initial_state, None, None)
    
    # if (isGoal(init_node.state)) then return init_node
    if init_node.state.isGoal():
        print("BFS: Initial state is goal!")
        return init_node, 0
    
    # Open.enqueue(init_node)
    open_list.append(init_node)
    
    # Closed <- [ ]
    steps = 0
    
    # while (not Open.empty()) do
    while open_list:
        # current <- Open.dequeue() /* Choose the shallowest node in Open */
        current = open_list.popleft()
        
        # Closed.add(current)
        closed_set.add(hash(current.state))
        steps += 1
        
        # for each (action, successor) in successorsFn(current.state) do
        for action, successor_state in current.state.successorFunction():
            # child <- Node (successor, current, action)
            child = Node(successor_state, current, action)
            
            # Check if state already visited
            child_hash = hash(child.state)
            
            # if (child.state not in Closed and not in Open) then
            # Check closed set
            if child_hash in closed_set:
                continue
            
            # Check open list
            already_in_open = any(hash(node.state) == child_hash for node in open_list)
            if already_in_open:
                continue
            
            # if (isGoal(child.state)) then return child
            if child.state.isGoal():
                print(f"BFS: Solution found in {steps} steps!")
                return child, steps
            
            # Open.enqueue(child)
            open_list.append(child)
    
    # return None
    print("BFS: No solution found!")
    return None, steps


def heuristic_h1(state):
    """
    Heuristic 1: Distance from red car 'X' to the exit.
    
    The exit is at position (board_width - 2, board_height/2 - 1).
    For a horizontal car, we calculate horizontal distance.
    """
    # Find the red car 'X'
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            target_x = state.board_width - 2
            current_x = vehicle['x']
            
            # Distance to exit
            distance = target_x - current_x
            return max(0, distance)  # Never negative
    
    return 0


def heuristic_h2(state):
    """
    Heuristic 2: h1 + number of blocking vehicles.
    
    Counts vehicles that block the red car's path to the exit.
    """
    h1 = heuristic_h1(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if not red_car:
        return h1
    
    # Count blocking vehicles (using a set to avoid double-counting)
    blocking_vehicles = set()
    red_y = red_car['y']
    red_x_end = red_car['x'] + red_car['length']
    target_x = state.board_width - 1  # Fixed: should be board_width - 1 (edge)
    
    # Check each position from red car end to exit
    for x in range(red_x_end, target_x):
        if x < state.board_width:
            cell = state.board[red_y][x]
            if cell != '.' and cell != '#' and cell != 'X':
                # There's a blocking vehicle
                blocking_vehicles.add(cell)
    
    return h1 + len(blocking_vehicles)


def heuristic_h3(state):
    """
    Heuristic 3: Enhanced heuristic considering blocking vehicles 
    and their mobility (proposed third heuristic).
    
    This heuristic adds penalties for:
    - Vehicles blocking the red car (h2)
    - Vehicles that are harder to move (blocked themselves)
    - Secondary blockers (vehicles blocking the primary blockers)
    """
    h2_value = heuristic_h2(state)
    
    # Find the red car
    red_car = None
    for vehicle in state.vehicles:
        if vehicle['id'] == 'X':
            red_car = vehicle
            break
    
    if not red_car:
        return h2_value
    
    # Additional penalty for deeply blocked vehicles
    penalty = 0
    red_y = red_car['y']
    red_x_end = red_car['x'] + red_car['length']
    target_x = state.board_width - 1
    
    # Find all blocking vehicles
    blocking_vehicle_ids = set()
    for x in range(red_x_end, target_x):
        if x < state.board_width:
            cell = state.board[red_y][x]
            if cell != '.' and cell != '#' and cell != 'X':
                blocking_vehicle_ids.add(cell)
    
    # Check blocking vehicles and their mobility
    for blocking_id in blocking_vehicle_ids:
        # Find this blocking vehicle
        for vehicle in state.vehicles:
            if vehicle['id'] == blocking_id:
                if vehicle['orientation'] == 'V':
                    # Vertical vehicle blocking horizontal path
                    # Check if it can move up or down
                    can_move_up = (vehicle['y'] > 0 and 
                                 state.board[vehicle['y'] - 1][vehicle['x']] == '.')
                    can_move_down = (vehicle['y'] + vehicle['length'] < state.board_height and 
                                   state.board[vehicle['y'] + vehicle['length']][vehicle['x']] == '.')
                    
                    if not (can_move_up or can_move_down):
                        # Vehicle is stuck, add higher penalty
                        penalty += 3
                    elif not can_move_up or not can_move_down:
                        # Vehicle can only move one direction
                        penalty += 1
                
                elif vehicle['orientation'] == 'H':
                    # Horizontal vehicle blocking (shouldn't happen but check anyway)
                    can_move_left = (vehicle['x'] > 0 and 
                                   state.board[vehicle['y']][vehicle['x'] - 1] == '.')
                    can_move_right = (vehicle['x'] + vehicle['length'] < state.board_width and 
                                    state.board[vehicle['y']][vehicle['x'] + vehicle['length']] == '.')
                    
                    if not (can_move_left or can_move_right):
                        penalty += 3
                    elif not can_move_left or not can_move_right:
                        penalty += 1
                break
    
    return h2_value + penalty


def A_star(initial_state, heuristic_function=heuristic_h1):
    """
    A* Search algorithm following the course pseudocode (Figure 1.29).
    Uses a heuristic function to guide the search.
    
    Parameters:
    - initial_state: RushHourPuzzle instance
    - heuristic_function: Function to estimate cost to goal
    
    Returns:
    - goal_node: Node containing the goal state, or None
    - steps: Number of nodes expanded
    """
    # Open: priorityQueue /* Ordered queue by f */
    open_list = []
    
    # Closed: list
    closed_set = set()
    
    # For tracking nodes in open list (for efficient lookup)
    open_dict = {}  # Maps state_hash -> (f_value, node)
    
    # init_node <- Node (s, None, None)
    init_node = Node(initial_state, None, None)
    
    # init_node.f <- h(init_node)
    init_node.setF(heuristic_function)
    
    # if (isGoal(init_node.state)) then return init_node
    if initial_state.isGoal():
        print("A*: Initial state is goal!")
        return init_node, 0
    
    # Open.insert(init_node)
    heapq.heappush(open_list, (init_node.f, id(init_node), init_node))
    open_dict[hash(init_node.state)] = (init_node.f, init_node)
    
    steps = 0
    
    # while (not Open.empty()) do
    while open_list:
        # current <- Open.dequeue() /* Choose the node with the lowest cost f */
        _, _, current = heapq.heappop(open_list)
        current_hash = hash(current.state)
        
        # Remove from open_dict if still there
        if current_hash in open_dict:
            del open_dict[current_hash]
        
        # if (isGoal(current.state)) then return current
        if current.state.isGoal():
            print(f"A*: Solution found in {steps} steps!")
            return current, steps
        
        # Closed.add(current)
        closed_set.add(current_hash)
        steps += 1
        
        # for each (action, successor) in successorsFn(current.state) do
        for action, successor_state in current.state.successorFunction():
            # child <- Node (successor, current, action)
            child = Node(successor_state, current, action)
            
            # child.f <- child.g + h(child)
            child.setF(heuristic_function)
            
            child_hash = hash(child.state)
            
            # if (child.state not in Open and not in Closed) then
            if child_hash not in closed_set and child_hash not in open_dict:
                # Open.insert(child)
                heapq.heappush(open_list, (child.f, id(child), child))
                open_dict[child_hash] = (child.f, child)
            
            # else if (child.state in Open with a higher value of f) then
            elif child_hash in open_dict:
                old_f, old_node = open_dict[child_hash]
                if child.f < old_f:
                    # replace that Open node with child
                    old_node.g = child.g
                    old_node.parent = child.parent
                    old_node.action = child.action
                    old_node.f = child.f
                    # Update in dictionary
                    open_dict[child_hash] = (child.f, old_node)
                    # Re-heapify (push the updated node)
                    heapq.heappush(open_list, (child.f, id(old_node), old_node))
            
            # else if (child.state in Closed with a higher value of f) then
            elif child_hash in closed_set:
                # In standard A* with consistent heuristic, this shouldn't happen
                # But we handle it for completeness
                # remove that Closed node and Open.insert(child)
                closed_set.remove(child_hash)
                heapq.heappush(open_list, (child.f, id(child), child))
                open_dict[child_hash] = (child.f, child)
    
    # return None
    print("A*: No solution found!")
    return None, steps