
Where:  
- `g(n)` = cost from start node to current node  
- `h(n)` = heuristic estimate of cost from current node to goal  

**Pros:** Optimal and complete if heuristic is admissible.  
**Cons:** Can be memory intensive.

---

## 2. Alpha-Beta Pruning
**Type:** Search Optimization (Game Trees)  
**Description:**  
Alpha-beta pruning is used to optimize **Minimax** algorithm by eliminating branches that do not affect the final decision.  
- `Alpha` = best value that maximizer can guarantee  
- `Beta` = best value that minimizer can guarantee  

**Pros:** Reduces number of nodes evaluated in a game tree.  
**Cons:** Works only with adversarial search.

---

## 3. A0 Star Search
**Type:** Special Case of A*  
**Description:**  
- A0 Star is similar to A* but typically assumes `h(n) = 0`, effectively behaving like **Uniform Cost Search**.  
- Guarantees optimal path but may explore more nodes.

---

## 4. Beam Search
**Type:** Heuristic Search  
**Description:**  
- Beam search explores a fixed number of best nodes at each level (beam width).  
- Not guaranteed to find the optimal solution but is memory-efficient.  

**Pros:** Efficient for large search spaces.  
**Cons:** May miss the optimal solution.

---

## 5. Best First Search
**Type:** Informed / Heuristic Search  
**Description:**  
- Chooses the node that appears to be closest to the goal using a heuristic function `h(n)`.  
- Can behave similarly to A* if combined with path cost.

**Pros:** Faster than uninformed searches.  
**Cons:** May not find optimal solution.

---

## 6. Breadth-First Search (BFS)
**Type:** Uninformed Search  
**Description:**  
- Explores all nodes level by level from the start node.  
- Guarantees the shortest path in unweighted graphs.  

**Pros:** Complete and optimal (for uniform cost).  
**Cons:** Memory-intensive for large graphs.

---

## 7. Depth-First Search (DFS)
**Type:** Uninformed Search  
**Description:**  
- Explores as far as possible along each branch before backtracking.  

**Pros:** Low memory usage.  
**Cons:** Not guaranteed to be optimal or complete (may get stuck in loops).

---

## 8. Bidirectional Search
**Type:** Uninformed Search  
**Description:**  
- Searches simultaneously from the start node and the goal node until the two meet.  
- Can reduce search time significantly.

**Pros:** Faster than BFS for large graphs.  
**Cons:** Requires knowledge of the goal in advance and can be memory-heavy.

---

## 9. Depth-Limited Search (DLS)
**Type:** Uninformed / DFS Variant  
**Description:**  
- DFS with a maximum depth limit to avoid infinite paths in cyclic graphs.  

**Pros:** Prevents infinite loops.  
**Cons:** May miss solutions beyond depth limit.

---

## 10. Iterative Deepening Search (IDS)
**Type:** Uninformed Search  
**Description:**  
- Repeatedly applies DLS with increasing depth limits.  
- Combines the benefits of BFS (completeness) and DFS (low memory).

**Pros:** Complete and memory-efficient.  
**Cons:** Some repeated exploration of nodes.

---