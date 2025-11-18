def alphabeta(depth, node_index, is_maximizing, values, alpha, beta, max_depth):
    if depth == max_depth:
        return values[node_index]

    if is_maximizing:
        best = float("-inf")
        for i in range(2):
            val = alphabeta(depth+1, node_index*2+i, False, values, alpha, beta, max_depth)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float("inf")
        for i in range(2):
            val = alphabeta(depth+1, node_index*2+i, True, values, alpha, beta, max_depth)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best



values = list(map(int, input("Enter leaf node values (space separated): ").split()))
import math
max_depth = int(math.log2(len(values)))
print("Optimal value (with pruning):", alphabeta(0, 0, True, values, -9999, 9999, max_depth))
