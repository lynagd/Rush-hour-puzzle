"""
Rush Hour Puzzle Solver
Main script to run the puzzle solver with different algorithms.
"""

from rush_hour_puzzle import RushHourPuzzle
from search_algorithms import BFS, A_star, heuristic_h1, heuristic_h2, heuristic_h3
from game_interface import visualize_solution
import time

def print_solution(solution_node):
    """Print the solution path and actions."""
    if solution_node is None:
        print("No solution found!")
        return
    
    print("\n" + "="*60)
    print("SOLUTION FOUND!")
    print("="*60)
    
    # Get solution details
    path = solution_node.getPath()
    actions = solution_node.getSolution()
    
    print(f"\nSolution length: {len(actions)} moves")
    print(f"Path cost: {solution_node.g}")
    
    print("\nSolution actions:")
    for i, action in enumerate(actions, 1):
        vehicle_id, direction = action
        direction_name = {
            'U': 'UP',
            'D': 'DOWN',
            'L': 'LEFT',
            'R': 'RIGHT'
        }
        print(f"  {i}. Move vehicle {vehicle_id} {direction_name[direction]}")
    
    print("\n" + "="*60)


def solve_puzzle(csv_file, use_visualization=True):
    """
    Solve a Rush Hour puzzle using different algorithms.
    
    Parameters:
    - csv_file: Path to CSV file with puzzle configuration
    - use_visualization: Whether to show Pygame visualization
    """
    print("\n" + "="*60)
    print(f"Loading puzzle from: {csv_file}")
    print("="*60)
    
    # Load the puzzle
    initial_state = RushHourPuzzle(csv_file=csv_file)
    
    print("\nInitial state:")
    print(initial_state)
    
    # Test if it's already a goal
    if initial_state.isGoal():
        print("Initial state is already a goal!")
        return
    
    # Dictionary to store results
    results = {}
    
    # ===== BFS Algorithm =====
    print("\n" + "-"*60)
    print("Running BFS Algorithm...")
    print("-"*60)
    start_time = time.time()
    bfs_solution, bfs_steps = BFS(initial_state)
    bfs_time = time.time() - start_time
    
    if bfs_solution:
        results['BFS'] = {
            'solution': bfs_solution,
            'steps': bfs_steps,
            'time': bfs_time,
            'cost': bfs_solution.g
        }
        print(f"✓ Solution found in {bfs_steps} search steps")
        print(f"✓ Solution cost: {bfs_solution.g} moves")
        print(f"✓ Time taken: {bfs_time:.4f} seconds")
    
    # ===== A* with h1 =====
    print("\n" + "-"*60)
    print("Running A* Algorithm with Heuristic h1...")
    print("(h1 = distance from red car to exit)")
    print("-"*60)
    start_time = time.time()
    astar_h1_solution, astar_h1_steps = A_star(initial_state, heuristic_h1)
    astar_h1_time = time.time() - start_time
    
    if astar_h1_solution:
        results['A* (h1)'] = {
            'solution': astar_h1_solution,
            'steps': astar_h1_steps,
            'time': astar_h1_time,
            'cost': astar_h1_solution.g
        }
        print(f"✓ Solution found in {astar_h1_steps} search steps")
        print(f"✓ Solution cost: {astar_h1_solution.g} moves")
        print(f"✓ Time taken: {astar_h1_time:.4f} seconds")
    
    # ===== A* with h2 =====
    print("\n" + "-"*60)
    print("Running A* Algorithm with Heuristic h2...")
    print("(h2 = h1 + number of blocking vehicles)")
    print("-"*60)
    start_time = time.time()
    astar_h2_solution, astar_h2_steps = A_star(initial_state, heuristic_h2)
    astar_h2_time = time.time() - start_time
    
    if astar_h2_solution:
        results['A* (h2)'] = {
            'solution': astar_h2_solution,
            'steps': astar_h2_steps,
            'time': astar_h2_time,
            'cost': astar_h2_solution.g
        }
        print(f"✓ Solution found in {astar_h2_steps} search steps")
        print(f"✓ Solution cost: {astar_h2_solution.g} moves")
        print(f"✓ Time taken: {astar_h2_time:.4f} seconds")
    
    # ===== A* with h3 =====
    print("\n" + "-"*60)
    print("Running A* Algorithm with Heuristic h3...")
    print("(h3 = h2 + penalty for stuck blocking vehicles)")
    print("-"*60)
    start_time = time.time()
    astar_h3_solution, astar_h3_steps = A_star(initial_state, heuristic_h3)
    astar_h3_time = time.time() - start_time
    
    if astar_h3_solution:
        results['A* (h3)'] = {
            'solution': astar_h3_solution,
            'steps': astar_h3_steps,
            'time': astar_h3_time,
            'cost': astar_h3_solution.g
        }
        print(f"✓ Solution found in {astar_h3_steps} search steps")
        print(f"✓ Solution cost: {astar_h3_solution.g} moves")
        print(f"✓ Time taken: {astar_h3_time:.4f} seconds")
    
    # ===== Comparison =====
    print("\n" + "="*60)
    print("ALGORITHM COMPARISON")
    print("="*60)
    print(f"{'Algorithm':<15} {'Search Steps':<15} {'Solution Cost':<15} {'Time (s)':<15}")
    print("-"*60)
    
    for algo_name, data in results.items():
        print(f"{algo_name:<15} {data['steps']:<15} {data['cost']:<15} {data['time']:<15.4f}")
    
    # Find best algorithm
    if results:
        best_algo = min(results.items(), key=lambda x: x[1]['steps'])
        print("\n" + "="*60)
        print(f"🏆 Most efficient: {best_algo[0]} with {best_algo[1]['steps']} search steps")
        print("="*60)
    
    # Show visualization
    if use_visualization and results:
        print("\n" + "="*60)
        print("VISUALIZATION")
        print("="*60)
        print("\nChoose algorithm to visualize:")
        print("1. BFS")
        print("2. A* with h1")
        print("3. A* with h2")
        print("4. A* with h3")
        
        choice = input("\nEnter choice (1-4, or press Enter for BFS): ").strip()
        
        algo_map = {
            '1': 'BFS',
            '2': 'A* (h1)',
            '3': 'A* (h2)',
            '4': 'A* (h3)',
            '': 'BFS'
        }
        
        selected_algo = algo_map.get(choice, 'BFS')
        
        if selected_algo in results:
            print(f"\nLaunching visualization for {selected_algo}...")
            print("\nControls:")
            print("  SPACE - Start/Stop animation")
            print("  LEFT/RIGHT ARROWS - Step through solution")
            print("  R - Reset to start")
            print("  ESC - Close window")
            
            data = results[selected_algo]
            visualize_solution(
                initial_state,
                data['solution'],
                selected_algo,
                data['steps']
            )


def main():
    """Main function."""
    print("\n" + "="*60)
    print(" "*15 + "RUSH HOUR PUZZLE SOLVER")
    print("="*60)
    
    # Example usage - you can change this path
    csv_file = "../examples/example1.csv"
    
    print("\nYou can solve different puzzles by changing the CSV file.")
    print(f"Currently using: {csv_file}")
    
    custom_file = input("\nEnter CSV file path (or press Enter to use default): ").strip()
    
    if custom_file:
        csv_file = custom_file
    
    try:
        solve_puzzle(csv_file, use_visualization=True)
    except FileNotFoundError:
        print(f"\n❌ Error: File '{csv_file}' not found!")
        print("Please make sure the file exists in the correct location.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()