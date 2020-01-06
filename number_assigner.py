from random import choice
from math import log10, floor


def select_node(assignment, mode):
    if mode == 1:
        pass #TODO: we should return base on MVR
    else: # We should choose randomly from unvisited nodes
        for i, val in enumerate(assignment):
            if val is None:
                return i
        

def consistent(assignment, node, node_type, edge):
    ntype = node_type[node]
    neighbour_value = 1 if ntype == 'T' or ntype == 'S' else 0
    valid = False
    for n in edge[node]:
        if assignment[n] is None:
            continue
        valid = True
        if ntype == 'T' or ntype == 'S':
            neighbour_value *= assignment[n]
        elif ntype == 'P' or ntype == 'H':
            neighbour_value += assignment[n]
    if valid:
        if ntype == 'T' or ntype == 'P':
            return assignment[node] != neighbour_value % 10
        elif ntype == 'S' or ntype == 'H':
            return assignment[node] != 10**floor(log10(neighbour_value))
    return True


def valid(assignment, node_type, node_num, edge):
    # At first we shuold check that each node has assigned with a value
    for n in range(node_num):
        if assignment[n] is None:
            return False
    # And then we should check that each assignment is consistent or not
    for n in range(node_num):
        if not consistent(assignment, n, node_type, edge):
            return False
    return True


def forward_check():
    pass


def backtrack(assignment, node_type, domain, node_num, edge, mode):
    if valid(assignment, node_type, node_num, edge): 
        return assignment
    if int(mode[1]) == 1:
        domain = forward_check() 
    n = select_node(assignment, mode=mode[0])
    for val in domain[n]:
        tmp_assignment = assignment[:]
        tmp_assignment[n] = val
        if consistent(tmp_assignment, n, node_type, edge):
            assignment[n] = val
            result = backtrack(assignment[:], node_type, domain[:], node_num, edge, mode)
            if result:
                return result
    return None


def initialize_list(node_num):
    l = []
    for i in range(node_num):
        l.append([])
    return l


def main():
    mode = "100"
    node_num = int(input())
    assignment = [None] * node_num

    edge_num = int(input())

    raw_node_type = input()
    node_type = raw_node_type.split(' ')

    edge = initialize_list(node_num)
    for _ in range(edge_num):
        e = list(map(int,input().split(' ')))
        edge[e[0]].append(e[1])
        edge[e[1]].append(e[0])

    domain = []
    for i in range(node_num):
        domain.append(list(range(1,10))) # Each node domain could be from 1 up to 9

    solution = backtrack(assignment[:], node_type, domain, node_num, edge, mode="100")
    if solution is not None:
        print(solution)


if __name__ == "__main__":
    main()