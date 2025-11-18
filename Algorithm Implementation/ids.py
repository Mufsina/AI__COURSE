def input_graph():
    graph = {}
    n = int(input("Enter number of nodes: "))
    for _ in range(n):
        node = input("Enter node name: ").strip()
        neighbors = input(f"Enter neighbors of {node} (space-separated): ").split()
        graph[node] = neighbors
    return graph

def dls(graph, node, goal, depth, path):
    if depth == 0 and node == goal:
        return path
    if depth > 0:
        for neighbor in graph.get(node, []):
            new_path = dls(graph, neighbor, goal, depth - 1, path + [neighbor])
            if new_path:
                return new_path
    return None

def ids(graph, start, goal, max_depth=10):
    for depth in range(max_depth):
        path = dls(graph, start, goal, depth, [start])
        if path:
            return path
    return None

if __name__ == "__main__":
    graph = input_graph()
    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()
    print("IDS Path:", ids(graph, start, goal))
