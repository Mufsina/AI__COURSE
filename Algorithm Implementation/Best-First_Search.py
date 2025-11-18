import heapq

def best_first_search(graph, start, goal, heuristic):
    visited = set()
    pq = [(heuristic[start], start)]  

    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        print("Visiting:", node)
        visited.add(node)

        if node == goal:
            print("Goal reached:", node)
            return True

        for neighbor in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (heuristic[neighbor], neighbor))
    return False



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

best_first_search(graph, start, goal, heuristic)
