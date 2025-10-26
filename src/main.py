"""
Rush Hour Puzzle Solver
<<<<<<< HEAD
Main script to run the puzzle solver with BFS and A* algorithms.
"""

from rush_hour_puzzle import RushHourPuzzle
from search_algorithms import BFS, A_star, heuristic_h1, heuristic_h2, heuristic_h3
from game_interface import visualize_solution
import time

def print_solution(solution_node, algorithm_name):
    """Print the solution path and actions."""
    if solution_node is None:
        print(f"No solution found for {algorithm_name}!")
        return
    
    print("\n" + "="*60)
    print(f"{algorithm_name} SOLUTION")
=======
Main script to run the puzzle solver with different algorithms.
"""

from rush_hour_puzzle import RushHourPuzzle
from search_algorithms import BFS
from game_interface import visualize_solution
import time

def print_solution(solution_node):
    """Print the solution path and actions."""
    if solution_node is None:
        print("No solution found!")
        return
    
    print("\n" + "="*60)
    print("SOLUTION FOUND!")
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
    print("="*60)
    
    # Get solution details
    path = solution_node.getPath()
    actions = solution_node.getSolution()
    
    print(f"\nSolution length: {len(actions)} moves")
<<<<<<< HEAD
    print(f"Path cost (g): {solution_node.g}")
    if hasattr(solution_node, 'f'):
        print(f"Total cost (f): {solution_node.f}")
=======
    print(f"Path cost: {solution_node.g}")
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
    
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


<<<<<<< HEAD
def solve_puzzle(csv_file, use_visualization=True, algorithms_to_run='all'):
=======
def solve_puzzle(csv_file, use_visualization=True):
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
    """
    Solve a Rush Hour puzzle using different algorithms.
    
    Parameters:
    - csv_file: Path to CSV file with puzzle configuration
    - use_visualization: Whether to show Pygame visualization
<<<<<<< HEAD
    - algorithms_to_run: 'all', 'bfs', 'astar', or list like ['bfs', 'astar_h1']
=======
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
    """
    print("\n" + "="*60)
    print(f"Loading puzzle from: {csv_file}")
    print("="*60)
    
    # Load the puzzle
    initial_state = RushHourPuzzle(csv_file=csv_file)
    
    print("\nInitial state:")
    print(initial_state)
    
<<<<<<< HEAD
    print(f"Board size: {initial_state.board_height}x{initial_state.board_width}")
    print(f"Number of vehicles: {len(initial_state.vehicles)}")
    print(f"Number of walls: {len(initial_state.walls)}")
    
    # Test if it's already a goal
    if initial_state.isGoal():
        print("\n⚠️  Initial state is already a goal!")
=======
    # Test if it's already a goal
    if initial_state.isGoal():
        print("Initial state is already a goal!")
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
        return
    
    # Dictionary to store results
    results = {}
    
<<<<<<< HEAD
    # Determine which algorithms to run
    run_bfs = algorithms_to_run == 'all' or 'bfs' in str(algorithms_to_run).lower()
    run_astar = algorithms_to_run == 'all' or 'astar' in str(algorithms_to_run).lower()
    
    # ===== BFS Algorithm =====
    if run_bfs:
        print("\n" + "="*60)
        print("RUNNING BFS ALGORITHM")
        print("="*60)
        print("BFS explores all nodes level by level (uninformed search)")
        print("Note: BFS may take longer on complex puzzles\n")
        
        start_time = time.time()
        try:
            bfs_solution, bfs_steps = BFS(initial_state)
            bfs_time = time.time() - start_time
            
            if bfs_solution:
                results['BFS'] = {
                    'solution': bfs_solution,
                    'steps': bfs_steps,
                    'time': bfs_time,
                    'cost': bfs_solution.g
                }
                print(f"✓ Solution found!")
                print(f"  - Search steps (nodes expanded): {bfs_steps}")
                print(f"  - Solution cost (moves): {bfs_solution.g}")
                print(f"  - Time taken: {bfs_time:.4f} seconds")
            else:
                print("✗ No solution found!")
        except KeyboardInterrupt:
            print("\n⚠️  BFS interrupted by user")
            run_astar = False  # Skip A* if user interrupted
        except Exception as e:
            print(f"✗ BFS failed with error: {e}")
    
    # ===== A* with h1 =====
    if run_astar:
        print("\n" + "="*60)
        print("RUNNING A* WITH HEURISTIC H1")
        print("="*60)
        print("h1 = distance from red car to exit")
        print("This is the simplest admissible heuristic\n")
        
        start_time = time.time()
        try:
            astar_h1_solution, astar_h1_steps = A_star(initial_state, heuristic_h1)
            astar_h1_time = time.time() - start_time
            
            if astar_h1_solution:
                results['A* (h1)'] = {
                    'solution': astar_h1_solution,
                    'steps': astar_h1_steps,
                    'time': astar_h1_time,
                    'cost': astar_h1_solution.g
                }
                print(f"✓ Solution found!")
                print(f"  - Search steps (nodes expanded): {astar_h1_steps}")
                print(f"  - Solution cost (moves): {astar_h1_solution.g}")
                print(f"  - Time taken: {astar_h1_time:.4f} seconds")
            else:
                print("✗ No solution found!")
        except KeyboardInterrupt:
            print("\n⚠️  A* (h1) interrupted by user")
            run_astar = False  # Skip remaining A* if user interrupted
        except Exception as e:
            print(f"✗ A* (h1) failed with error: {e}")
    
    # ===== A* with h2 =====
    if run_astar:
        print("\n" + "="*60)
        print("RUNNING A* WITH HEURISTIC H2")
        print("="*60)
        print("h2 = h1 + number of blocking vehicles")
        print("More informed than h1, should expand fewer nodes\n")
        
        start_time = time.time()
        try:
            astar_h2_solution, astar_h2_steps = A_star(initial_state, heuristic_h2)
            astar_h2_time = time.time() - start_time
            
            if astar_h2_solution:
                results['A* (h2)'] = {
                    'solution': astar_h2_solution,
                    'steps': astar_h2_steps,
                    'time': astar_h2_time,
                    'cost': astar_h2_solution.g
                }
                print(f"✓ Solution found!")
                print(f"  - Search steps (nodes expanded): {astar_h2_steps}")
                print(f"  - Solution cost (moves): {astar_h2_solution.g}")
                print(f"  - Time taken: {astar_h2_time:.4f} seconds")
            else:
                print("✗ No solution found!")
        except KeyboardInterrupt:
            print("\n⚠️  A* (h2) interrupted by user")
            run_astar = False  # Skip remaining A* if user interrupted
        except Exception as e:
            print(f"✗ A* (h2) failed with error: {e}")
    
    # ===== A* with h3 =====
    if run_astar:
        print("\n" + "="*60)
        print("RUNNING A* WITH HEURISTIC H3")
        print("="*60)
        print("h3 = h2 + penalties for blocked vehicles")
        print("Most informed heuristic (may not be admissible)\n")
        
        start_time = time.time()
        try:
            astar_h3_solution, astar_h3_steps = A_star(initial_state, heuristic_h3)
            astar_h3_time = time.time() - start_time
            
            if astar_h3_solution:
                results['A* (h3)'] = {
                    'solution': astar_h3_solution,
                    'steps': astar_h3_steps,
                    'time': astar_h3_time,
                    'cost': astar_h3_solution.g
                }
                print(f"✓ Solution found!")
                print(f"  - Search steps (nodes expanded): {astar_h3_steps}")
                print(f"  - Solution cost (moves): {astar_h3_solution.g}")
                print(f"  - Time taken: {astar_h3_time:.4f} seconds")
            else:
                print("✗ No solution found!")
        except KeyboardInterrupt:
            print("\n⚠️  A* (h3) interrupted by user")
        except Exception as e:
            print(f"✗ A* (h3) failed with error: {e}")
    
    # ===== Comparison Table =====
    if results:
        print("\n" + "="*60)
        print("ALGORITHM COMPARISON")
        print("="*60)
        print(f"{'Algorithm':<15} {'Nodes Expanded':<18} {'Solution Cost':<18} {'Time (s)':<15}")
        print("-"*66)
        
        for algo_name, data in results.items():
            print(f"{algo_name:<15} {data['steps']:<18} {data['cost']:<18} {data['time']:<15.4f}")
        
        # Analysis
        print("\n" + "="*60)
        print("ANALYSIS")
        print("="*60)
        
        # Find most efficient (fewest nodes expanded)
        best_efficiency = min(results.items(), key=lambda x: x[1]['steps'])
        print(f"🏆 Most efficient (fewest nodes): {best_efficiency[0]} with {best_efficiency[1]['steps']} nodes")
        
        # Find fastest
        fastest = min(results.items(), key=lambda x: x[1]['time'])
        print(f"⚡ Fastest execution: {fastest[0]} with {fastest[1]['time']:.4f} seconds")
        
        # Check solution optimality
        solution_costs = {name: data['cost'] for name, data in results.items()}
        min_cost = min(solution_costs.values())
        optimal_algorithms = [name for name, cost in solution_costs.items() if cost == min_cost]
        
        print(f"🎯 Optimal solution cost: {min_cost} moves")
        print(f"   Found by: {', '.join(optimal_algorithms)}")
        
        # Heuristic effectiveness comparison (if A* algorithms were run)
        astar_results = {k: v for k, v in results.items() if k.startswith('A*')}
        if len(astar_results) > 1:
            print("\n" + "-"*60)
            print("HEURISTIC EFFECTIVENESS (fewer nodes = better heuristic)")
            print("-"*60)
            sorted_astar = sorted(astar_results.items(), key=lambda x: x[1]['steps'])
            for i, (name, data) in enumerate(sorted_astar, 1):
                efficiency_vs_bfs = ""
                if 'BFS' in results:
                    reduction = ((results['BFS']['steps'] - data['steps']) / results['BFS']['steps']) * 100
                    efficiency_vs_bfs = f" ({reduction:+.1f}% vs BFS)"
                print(f"{i}. {name}: {data['steps']} nodes{efficiency_vs_bfs}")
        
        print("="*60)
    
    # ===== Visualization =====
    if use_visualization and results:
        print("\n" + "="*60)
        print("VISUALIZATION")
        print("="*60)
        
        # Choose algorithm for visualization
        if len(results) == 1:
            # Only one algorithm ran, use it
            chosen_algo = list(results.keys())[0]
        else:
            # Let user choose which solution to visualize
            print("\nAvailable solutions to visualize:")
            algo_list = list(results.keys())
            for i, algo_name in enumerate(algo_list, 1):
                print(f"  {i}. {algo_name} ({results[algo_name]['cost']} moves, {results[algo_name]['steps']} nodes)")
            
            # Choose best algorithm (fewest nodes) by default
            default_algo = best_efficiency[0] if 'best_efficiency' in locals() else algo_list[0]
            
            choice = input(f"\nEnter number to visualize (or press Enter for {default_algo}): ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(algo_list):
                chosen_algo = algo_list[int(choice) - 1]
            else:
                chosen_algo = default_algo
        
=======
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
    
    # NOTE: A* runs are intentionally disabled/commented out so only BFS is executed.
    # If you want to re-enable A*, restore the imports at top and the blocks below.
    
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
    
    # Show visualization (BFS only)
    if use_visualization and 'BFS' in results:
        print("\n" + "="*60)
        print("VISUALIZATION")
        print("="*60)
        print("\nLaunching visualization for BFS...")
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
        print("\nControls:")
        print("  SPACE - Start/Stop animation")
        print("  LEFT/RIGHT ARROWS - Step through solution")
        print("  R - Reset to start")
        print("  ESC - Close window")
        
<<<<<<< HEAD
        print(f"\nLaunching visualization for {chosen_algo}...")
        data = results[chosen_algo]
        
        try:
            visualize_solution(
                initial_state,
                data['solution'],
                chosen_algo,
                data['steps']
            )
        except Exception as e:
            print(f"⚠️  Visualization error: {e}")
            print("Make sure pygame is properly installed")
=======
        data = results['BFS']
        visualize_solution(
            initial_state,
            data['solution'],
            'BFS',
            data['steps']
        )
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395


def main():
    """Main function."""
    print("\n" + "="*60)
    print(" "*15 + "RUSH HOUR PUZZLE SOLVER")
<<<<<<< HEAD
    print(" "*10 + "BFS and A* with Multiple Heuristics")
    print("="*60)
    
    # Use example1.csv as default (same as main.py for consistency)
    default_csv = "./examples/2-d.csv"
    
    print("\n📁 CSV File Selection")
    print(f"Default: {default_csv}")
    print("\nAvailable examples:")
    print("  - examples/example1.csv (simple, fast)")
    print("  - examples/2-a.csv through 2-f.csv (more complex)")
    
    custom_file = input("\nEnter CSV file path (or press Enter for default): ").strip()
    
    csv_file = custom_file if custom_file else default_csv
    
    # Algorithm selection
    print("\n🔍 Algorithm Selection")
    print("1. Run all algorithms (BFS + A* with h1, h2, h3)")
    print("2. Run only BFS")
    print("3. Run only A* algorithms")
    
    algo_choice = input("\nEnter choice (default: 1): ").strip()
    
    if algo_choice == '2':
        algorithms_to_run = 'bfs'
    elif algo_choice == '3':
        algorithms_to_run = 'astar'
    else:
        algorithms_to_run = 'all'
    
    # Visualization option
    visualize = input("\n🎮 Enable visualization? (y/n, default: y): ").strip().lower()
    use_visualization = visualize != 'n'
    
    print("\n" + "="*60)
    print("Starting solver...")
    print("="*60)
    
    try:
        solve_puzzle(csv_file, use_visualization, algorithms_to_run)
        
        print("\n✅ Execution completed successfully!")
        
    except FileNotFoundError:
        print(f"\n❌ Error: File '{csv_file}' not found!")
        print("Please make sure the file exists in the correct location.")
        print("\nExpected CSV format:")
        print("  Line 1: board_height,board_width")
        print("  Other lines: vehicle_id,x,y,orientation,length")
        print("  Walls: #,x,y")
        
=======
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
>>>>>>> 24cce4b5f5de41790348903ec88c5fb315c7e395
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()