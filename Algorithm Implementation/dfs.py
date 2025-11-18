def input_graph():
    graph = {}
    n = int(input("Enter number of nodes: "))
    for _ in range(n):
        node = input("Enter node name: ").strip()
        neighbors = input(f"Enter neighbors of {node} (space-separated): ").split()
        graph[node] = neighbors
    return graph

def dfs(graph, start, goal, visited=None, path=None):
    if visited is None:
        visited = []
    if path is None:
        path = [start]

    visited.append(start)

    if start == goal:
        return path

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            new_path = dfs(graph, neighbor, goal, visited, path + [neighbor])
            if new_path:
                return new_path
    return None

if __name__ == "__main__":
    graph = input_graph()
    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()
    print("DFS Path:", dfs(graph, start, goal))
