from collections import deque

def input_graph():
    graph = {}
    n = int(input("Enter number of nodes: "))
    for _ in range(n):
        node = input("Enter node name: ").strip()
        neighbors = input(f"Enter neighbors of {node} (space-separated): ").split()
        graph[node] = neighbors
    return graph

def bfs(graph, start, goal):
    visited = []
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            visited.append(node)
            if node == goal:
                return path

            for neighbor in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

if __name__ == "__main__":
    graph = input_graph()
    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()
    print("BFS Path:", bfs(graph, start, goal))
