# test_bfs.py
from rush_hour_puzzle import RushHourPuzzle
from algo import bfs

# A list of CSV filenames you want to test
csv_files = [
    "examples/2-a.csv",
    "examples/2-b.csv",
    "examples/2-c.csv",
    "examples/2-d.csv",
    "examples/2-e.csv",
    "examples/e-f.csv"
]

# Loop through each file and try the BFS algorithm
for csv_file in csv_files:
    print("=" * 50)
    print(f"🔹 Testing file: {csv_file}")
    
    # Load the puzzle from the CSV
    puzzle = RushHourPuzzle(csv_file=csv_file)
    
    # Print the initial board
    print("Initial board:")
    print(puzzle)

    # Run BFS to find a solution
    goal_node = bfs(puzzle)

    # Check if a solution was found
    if goal_node:
        print("Solution found!")
        print("Moves to solve:", goal_node.getSolution())
        print("Number of moves:", len(goal_node.getSolution()))
        print("Final board:")
        print(goal_node.state)
    else:
        print("No solution found for this puzzle.")
    
    print("=" * 50)
