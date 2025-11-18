def input_graph():
    graph = {}
    n = int(input("Enter number of nodes: "))
    for _ in range(n):
        node = input("Enter node name: ").strip()
        neighbors = input(f"Enter neighbors of {node} (space-separated): ").split()
        graph[node] = neighbors
    return graph


def depth_limited_search(graph, node, goal, limit, path=None):
    if path is None:
        path = [node]

    if node == goal:
        return path

    if limit <= 0:
        return None

    for neighbor in graph.get(node, []):
        new_path = depth_limited_search(graph, neighbor, goal, limit - 1, path + [neighbor])
        if new_path:
            return new_path

    return None


if __name__ == "__main__":
    graph = input_graph()
    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()
    limit = int(input("Enter depth limit: "))

    result = depth_limited_search(graph, start, goal, limit)

    if result:
        print("Path Found:", result)
    else:
        print("No path found within the given depth limit.")
