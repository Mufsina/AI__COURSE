def input_graph():
    graph = {}
    n = int(input("Enter number of nodes: "))
    for _ in range(n):
        node = input("Enter node name: ").strip()
        neighbors = input(f"Enter neighbors of {node} (space-separated): ").split()
        graph[node] = neighbors
    return graph

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]

    front_start = {start: [start]}
    front_goal = {goal: [goal]}

    while front_start and front_goal:
        # Expand from start side
        new_front_start = {}
        for node, path in front_start.items():
            for neighbor in graph.get(node, []):
                if neighbor not in front_start:
                    new_path = path + [neighbor]
                    new_front_start[neighbor] = new_path
                    if neighbor in front_goal:
                        return new_path[:-1] + front_goal[neighbor][::-1]
        front_start.update(new_front_start)

        # Expand from goal side
        new_front_goal = {}
        for node, path in front_goal.items():
            for neighbor in graph.get(node, []):
                if neighbor not in front_goal:
                    new_path = path + [neighbor]
                    new_front_goal[neighbor] = new_path
                    if neighbor in front_start:
                        return front_start[neighbor][:-1] + new_path[::-1]
        front_goal.update(new_front_goal)

    return None

if __name__ == "__main__":
    graph = input_graph()
    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()
    print("Bidirectional Path:", bidirectional_search(graph, start, goal))
