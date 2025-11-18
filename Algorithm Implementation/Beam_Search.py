def beam_search(graph, start, goal, heuristic, beam_width):
    frontier = [(heuristic[start], start)]
    while frontier:
        new_frontier = []
        for _, node in frontier:
            print("Visiting:", node)
            if node == goal:
                print("Goal reached:", node)
                return True
            for neighbor in graph[node]:
                new_frontier.append((heuristic[neighbor], neighbor))
        frontier = sorted(new_frontier)[:beam_width]
    return False


# ---------------- User Input ----------------
n = int(input("Enter number of nodes: "))
graph = {}
heuristic = {}

for i in range(n):
    node = input(f"Enter node name {i+1}: ")
    neighbors = input(f"Enter neighbors of {node} (space separated): ").split()
    graph[node] = neighbors
    heuristic[node] = int(input(f"Heuristic value of {node}: "))

start = input("Enter start node: ")
goal = input("Enter goal node: ")
beam_width = int(input("Enter beam width: "))

beam_search(graph, start, goal, heuristic, beam_width)
