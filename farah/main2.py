from rush_hour_puzzle import RushHourPuzzle
from algo import bfs

# Load puzzle
puzzle = RushHourPuzzle(csv_file="examples/2-b.csv")

print("Initial state:")
print(puzzle)

# Run BFS
solution_node = bfs(puzzle)

if solution_node:
    print(f"\nSolution found in {solution_node.g} moves!")
    print("Moves:", solution_node.getSolution())
    

else:
    print("No solution exists!")