def data_dynamic(filename):
    items = []
    sorce = open(filename, "r")
    first_line = sorce.readline().strip()
    split_line = first_line.split()
    n = int(split_line[0])
    capacity = int(split_line[1])

    for line in range(n):
        current_line = sorce.readline().strip()
        split_line = current_line.split()
        weight = int(split_line[0])
        value = int(split_line[1])
        items.append((weight, value))
    
    sorce.close()
    return n, capacity, items


def dynamic_backpack(n, capacity, items):
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    chosen_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen_items.append(i - 1)
            w -= items[i - 1][0]
    chosen_items.reverse()
    
    
    return dp[n][capacity], chosen_items

   


