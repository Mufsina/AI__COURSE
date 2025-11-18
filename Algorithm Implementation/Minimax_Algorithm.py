def minimax(depth, node_index, is_maximizing, values, max_depth):
    if depth == max_depth:
        return values[node_index]

    if is_maximizing:
        return max(minimax(depth+1, node_index*2, False, values, max_depth),
                   minimax(depth+1, node_index*2+1, False, values, max_depth))
    else:
        return min(minimax(depth+1, node_index*2, True, values, max_depth),
                   minimax(depth+1, node_index*2+1, True, values, max_depth))


# --- User Input ---
values = list(map(int, input("Enter leaf node values (space separated): ").split()))
import math
max_depth = int(math.log2(len(values)))
print("Optimal value:", minimax(0, 0, True, values, max_depth))
