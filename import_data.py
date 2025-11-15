def data(filename):
    items = []
    sorce  = open(filename, "r")
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


