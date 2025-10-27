from rush_hour_puzzle import RushHourPuzzle
from search_algorithms import BFS, A_star, heuristic_h1, heuristic_h2, heuristic_h3
from game_interface import visualize_solution
import time
import os


# ALGORITHM CONFIGURATION

# Easy to add new algorithms - just add to this dictionary!
ALGORITHMS = {
    'BFS': {
        'name': 'BFS',
        'description': 'Breadth-First Search (uninformed)',
        'function': BFS,
        'heuristic': None,
        'note': 'May be slow on complex puzzles'
    },
    'A* (h1)': {
        'name': 'A* (h1)',
        'description': 'A* with h1: distance to exit',
        'function': A_star,
        'heuristic': heuristic_h1,
        'note': 'Simple admissible heuristic'
    },
    'A* (h2)': {
        'name': 'A* (h2)',
        'description': 'A* with h2: h1 + blocking vehicles',
        'function': A_star,
        'heuristic': heuristic_h2,
        'note': 'More informed than h1'
    },
    'A* (h3)': {
        'name': 'A* (h3)',
        'description': 'A* with h3: h2 + secondary blockers',
        'function': A_star,
        'heuristic': heuristic_h3,
        'note': 'Most sophisticated heuristic'
    }
}


# HELPER FUNCTIONS
def print_header(text, width=60):
    """Print a formatted header."""
    print("\n" + "="*width)
    print(text.center(width) if len(text) < width-4 else text)
    print("="*width)


def print_subheader(text, width=60):
    """Print a formatted subheader."""
    print("\n" + "-"*width)
    print(f" {text}")
    print("-"*width)


def load_puzzle(csv_file):
    """
    Load puzzle from CSV file with validation.
    
    Returns:
        RushHourPuzzle instance or None if failed
    """
    try:
        puzzle = RushHourPuzzle(csv_file=csv_file)
        
        print_subheader("Puzzle Information")
        print(f"File: {csv_file}")
        print(f"Board size: {puzzle.board_height}×{puzzle.board_width}")
        print(f"Vehicles: {len(puzzle.vehicles)}")
        print(f"Walls: {len(puzzle.walls)}")
        
        print("\nInitial state:")
        print(puzzle)
        
        # Check if already solved
        if puzzle.isGoal():
            print("⚠️  This puzzle is already solved!")
            return None
        
        return puzzle
        
    except FileNotFoundError:
        print(f"\n❌ Error: File '{csv_file}' not found!")
        print("\nExpected CSV format:")
        print("  Line 1: board_height,board_width")
        print("  Line 2+: vehicle_id,x,y,orientation,length")
        print("  Walls: #,x,y")
        return None
        
    except Exception as e:
        print(f"\n❌ Error loading puzzle: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_algorithm(algo_config, initial_state):
    """
    Run a single algorithm and return results.
    
    This function replaces 4 repeated code blocks with one clean function!
    
    Parameters:
        algo_config: Dictionary with algorithm configuration
        initial_state: Puzzle state to solve
    
    Returns:
        Dictionary with results or None if failed
    """
    name = algo_config['name']
    description = algo_config['description']
    function = algo_config['function']
    heuristic = algo_config['heuristic']
    note = algo_config.get('note', '')
    
    # Print algorithm info
    print_subheader(f"RUNNING {name}")
    print(f"Strategy: {description}")
    if note:
        print(f"Note: {note}")
    print()  # Blank line for readability
    
    # Run the algorithm
    start_time = time.time()
    
    try:
        # Call with or without heuristic
        if heuristic:
            solution, steps = function(initial_state, heuristic)
        else:
            solution, steps = function(initial_state)
        
        elapsed_time = time.time() - start_time
        
        # Check if solution found
        if solution:
            print(f"✓ Solution found!")
            print(f"  • Nodes expanded: {steps:,}")
            print(f"  • Solution cost: {solution.g} moves")
            print(f"  • Time: {elapsed_time:.4f} seconds")
            
            return {
                'solution': solution,
                'steps': steps,
                'time': elapsed_time,
                'cost': solution.g
            }
        else:
            print(f"✗ No solution found after {steps:,} nodes")
            return None
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user (Ctrl+C)")
        raise  # Re-raise to stop other algorithms
    
    except Exception as e:
        print(f"✗ Algorithm failed: {e}")
        return None


def run_all_algorithms(initial_state, algorithm_choice):
    """
    Run selected algorithms on the puzzle.
    
    Parameters:
        initial_state: Puzzle to solve
        algorithm_choice: 'all', 'bfs', or 'astar'
    
    Returns:
        Dictionary of results {algo_name: result_dict}
    """
    print_header("RUNNING ALGORITHMS")
    
    results = {}
    
    # Determine which algorithms to run
    algorithms_to_run = []
    
    if algorithm_choice == 'all':
        algorithms_to_run = list(ALGORITHMS.keys())
    elif algorithm_choice == 'bfs':
        algorithms_to_run = ['BFS']
    elif algorithm_choice == 'astar':
        algorithms_to_run = [k for k in ALGORITHMS.keys() if k.startswith('A*')]
    
    # Run each algorithm
    for algo_name in algorithms_to_run:
        try:
            result = run_algorithm(ALGORITHMS[algo_name], initial_state)
            if result:
                results[algo_name] = result
        
        except KeyboardInterrupt:
            print(f"\n⚠️  Stopping after {len(results)} algorithm(s) completed")
            break
    
    return results


def print_comparison_table(results):
    """
    Print a comparison table of all algorithm results.
    
    Much cleaner than scattered print statements!
    """
    if not results:
        print("\n⚠️  No results to compare")
        return
    
    print_header("ALGORITHM COMPARISON")
    
    # Table header
    print(f"\n{'Algorithm':<15} {'Nodes':<12} {'Moves':<10} {'Time (s)':<12} {'Efficiency':<12}")
    print("-"*61)
    
    # Table rows
    for algo_name, data in results.items():
        efficiency = f"{data['steps']/data['cost']:.1f}" if data['cost'] > 0 else "N/A"
        print(f"{algo_name:<15} {data['steps']:<12,} {data['cost']:<10} "
              f"{data['time']:<12.4f} {efficiency:<12}")


def print_analysis(results):
    """
    Analyze and print insights about the results.
    
    Shows which algorithm was best in different metrics.
    """
    if not results:
        return
    
    print_header("PERFORMANCE ANALYSIS")
    
    # Most efficient (fewest nodes)
    best_efficiency = min(results.items(), key=lambda x: x[1]['steps'])
    print(f"\n🏆 Most Efficient (fewest nodes):")
    print(f"   {best_efficiency[0]} - {best_efficiency[1]['steps']:,} nodes")
    
    # Fastest execution
    fastest = min(results.items(), key=lambda x: x[1]['time'])
    print(f"\n⚡ Fastest Execution:")
    print(f"   {fastest[0]} - {fastest[1]['time']:.4f} seconds")
    
    # Optimal solution
    min_cost = min(data['cost'] for data in results.values())
    optimal_algos = [name for name, data in results.items() if data['cost'] == min_cost]
    print(f"\n🎯 Optimal Solution Cost: {min_cost} moves")
    print(f"   Found by: {', '.join(optimal_algos)}")
    
    # Heuristic comparison (if multiple A* algorithms ran)
    astar_results = {k: v for k, v in results.items() if k.startswith('A*')}
    if len(astar_results) > 1:
        print(f"\n📈 Heuristic Effectiveness (fewer nodes = better):")
        sorted_astar = sorted(astar_results.items(), key=lambda x: x[1]['steps'])
        
        for i, (name, data) in enumerate(sorted_astar, 1):
            efficiency_gain = ""
            if 'BFS' in results:
                reduction = ((results['BFS']['steps'] - data['steps']) / results['BFS']['steps']) * 100
                efficiency_gain = f" ({reduction:+.1f}% vs BFS)"
            print(f"   {i}. {name}: {data['steps']:,} nodes{efficiency_gain}")


def select_for_visualization(results):
    """
    Let user select which algorithm solution to visualize.
    
    Returns:
        Tuple of (algo_name, result_data) or (None, None) if cancelled
    """
    if not results:
        return None, None
    
    print_header("VISUALIZATION")
    
    # If only one result, auto-select it
    if len(results) == 1:
        algo_name = list(results.keys())[0]
        print(f"\nAutomatically selected: {algo_name}")
        return algo_name, results[algo_name]
    
    # Multiple results - let user choose
    print("\n📺 Available solutions:")
    algo_list = list(results.keys())
    
    for i, algo_name in enumerate(algo_list, 1):
        data = results[algo_name]
        print(f"  {i}. {algo_name:<15} ({data['cost']} moves, {data['steps']:,} nodes)")
    
    # Recommend most efficient
    best = min(results.items(), key=lambda x: x[1]['steps'])
    print(f"\n💡 Recommendation: {best[0]} (most efficient)")
    
    # Get user choice
    choice = input(f"\nSelect algorithm (1-{len(algo_list)}, or Enter for recommendation): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(algo_list):
        chosen_algo = algo_list[int(choice) - 1]
    else:
        chosen_algo = best[0]
    
    print(f"\n✓ Selected: {chosen_algo}")
    return chosen_algo, results[chosen_algo]


def visualize_solution_safe(initial_state, algo_name, result_data):
    """
    Safely launch visualization with error handling.
    """
    print("\n🎮 Controls:")
    print("  • SPACE - Start/Stop animation")
    print("  • LEFT/RIGHT ARROWS - Step through solution")
    print("  • R - Reset to start")
    print("  • ESC - Close window")
    
    print(f"\n🚀 Launching visualization...")
    
    try:
        visualize_solution(
            initial_state,
            result_data['solution'],
            algo_name,
            result_data['steps']
        )
    except Exception as e:
        print(f"\n⚠️  Visualization error: {e}")
        print("Make sure pygame is installed: pip install pygame")


def get_csv_file():
    """
    Get CSV file from user with smart defaults.
    
    Returns:
        Path to CSV file
    """
    print_header("CSV FILE SELECTION")
    
    default_csv = "./examples/example1.csv"
    
    # Check for available files
    example_files = []
    if os.path.exists("./examples"):
        for filename in os.listdir("./examples"):
            if filename.endswith('.csv'):
                example_files.append(f"./examples/{filename}")
        example_files.sort()
    
    # Display options
    if example_files:
        print("\n📋 Available puzzle files:")
        for i, filepath in enumerate(example_files, 1):
            status = " (default)" if filepath == default_csv else ""
            print(f"  {i}. {filepath}{status}")
    
    print(f"\n💡 Or enter a custom path")
    
    # Get user input
    choice = input(f"\nEnter file (1-{len(example_files)} or path, Enter for default): ").strip()
    
    if not choice:
        return default_csv
    elif choice.isdigit() and 1 <= int(choice) <= len(example_files):
        return example_files[int(choice) - 1]
    else:
        return choice


def get_algorithm_choice():
    """
    Get which algorithms to run from user.
    
    Returns:
        String: 'all', 'bfs', or 'astar'
    """
    print_header("ALGORITHM SELECTION")
    
    print("\n📊 Available options:")
    print("  1. Run all algorithms (BFS + A* with h1, h2, h3)")
    print("  2. Run only BFS")
    print("  3. Run only A* algorithms (h1, h2, h3)")
    
    choice = input("\nEnter choice (1-3, default: 1): ").strip()
    
    if choice == '2':
        return 'bfs'
    elif choice == '3':
        return 'astar'
    else:
        return 'all'


def get_visualization_preference():
    """
    Ask if user wants visualization.
    
    Returns:
        Boolean: True if user wants visualization
    """
    print_header("VISUALIZATION")
    
    choice = input("\n🎮 Enable Pygame visualization? (y/n, default: y): ").strip().lower()
    return choice != 'n'


# MAIN SOLVER FUNCTION
def solve_puzzle(csv_file, algorithm_choice, use_visualization):
    """
    Main solver function - orchestrates the entire solving process.
    
    This is now clean and easy to follow!
    
    Steps:
    1. Load puzzle
    2. Run algorithms
    3. Show comparison
    4. Visualize solution
    """
    print_header("LOADING PUZZLE")
    
    # Step 1: Load puzzle
    initial_state = load_puzzle(csv_file)
    if not initial_state:
        return  # Error already printed in load_puzzle()
    
    # Step 2: Run algorithms
    results = run_all_algorithms(initial_state, algorithm_choice)
    
    if not results:
        print("\n⚠️  No algorithms completed successfully")
        return
    
    # Step 3: Show comparison and analysis
    print_comparison_table(results)
    print_analysis(results)
    
    # Step 4: Visualization (if requested)
    if use_visualization:
        algo_name, result_data = select_for_visualization(results)
        if algo_name:
            visualize_solution_safe(initial_state, algo_name, result_data)


# MAIN ENTRY POINT
def main():
    """
    Main entry point - keeps everything simple and clean.
    
    Now this is just 3 function calls!
    """
    # Welcome message
    print("\n" + "="*60)
    print("🚗 RUSH HOUR PUZZLE SOLVER 🚗".center(60))
    print("BFS and A* with Multiple Heuristics".center(60))
    print("="*60)
    
    try:
        # Get user preferences
        csv_file = get_csv_file()
        algorithm_choice = get_algorithm_choice()
        use_visualization = get_visualization_preference()
        
        # Solve the puzzle
        solve_puzzle(csv_file, algorithm_choice, use_visualization)
        
        # Success message
        print_header("EXECUTION COMPLETED")
        print("\n✅ Thank you for using Rush Hour Solver!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user. Goodbye!")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()