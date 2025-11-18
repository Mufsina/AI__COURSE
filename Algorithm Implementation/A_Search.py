import heapq

def a_star(graph, start, goal, heuristic, cost):
    pq = [(heuristic[start], 0, start)] 
    visited = {}

    while pq:
        f, g, node = heapq.heappop(pq)
        if node in visited and visited[node] <= g:
            continue
        print("Visiting:", node)
        visited[node] = g

        if node == goal:
            print("Goal reached:", node, "with cost:", g)
            return g

        for neighbor in graph[node]:
            new_g = g + cost[(node, neighbor)]
            heapq.heappush(pq, (new_g + heuristic[neighbor], new_g, neighbor))
    return float("inf")



n = int(input("Enter number of nodes: "))
graph = {}
heuristic = {}

for i in range(n):
    node = input(f"Enter node name {i+1}: ")
    neighbors = input(f"Enter neighbors of {node} (space separated): ").split()
    graph[node] = neighbors
    heuristic[node] = int(input(f"Heuristic value of {node}: "))

m = int(input("Enter number of edges with cost: "))
cost = {}
for _ in range(m):
    u, v, c = input("Enter edge (u v cost): ").split()
    cost[(u, v)] = int(c)

start = input("Enter start node: ")
goal = input("Enter goal node: ")

a_star(graph, start, goal, heuristic, cost)
