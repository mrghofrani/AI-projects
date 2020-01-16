from random import choice
from math import log10, floor
from operator import __add__, __mul__


def select_node(assignment, domain, mode):
    if mode[0] == '1':
        min_val = float("inf")
        for i, _ in enumerate(domain):
            if assignment[i] is None and domain[i] is not None:
                if min_val > len(domain[i]):
                    min_val = len(domain[i])
                    index = i
        return index
    else: # We should choose randomly from unvisited nodes
        for i, val in enumerate(assignment):
            if val is None:
                return i
        

def consistent(assignment, node, node_type, edge):
    ntype = node_type[node]
    if ntype == 'C':
        return True # There is no consistent checking for circle
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
        if ntype == 'S' or ntype == 'H':
            return assignment[node] == neighbour_value % 10
        elif ntype == 'T' or ntype == 'P':
            return assignment[node] == neighbour_value // 10**floor(log10(neighbour_value))
    return True


def valid(assignment, node_type, edge):
    # At first we shuold check that each node has assigned with a value

    for i,_ in enumerate(node_type):
        if assignment[i] is None:
            return False
    # And then we should check that each assignment is consistent or not
    for i,_ in enumerate(node_type):
        if not consistent(assignment, i, node_type, edge):
            return False
    return True


def constrainter(assignment, node, domain, edge, node_type):

    # Setting each edge to a category
    assigned = []
    unassigned = []
    for n in edge[node]:
        if assignment[n] is None:
            unassigned.append(n)
        else:
            assigned.append(n)
    
    if node_type == 'T' or node_type == 'S': 
        func = __mul__
        store = 1
    elif node_type == 'H' or node_type == 'P':
        func = __add__
        store = 0
    elif node_type == 'C':
        return

    if not unassigned: # if all adjacends where assigned with a number
        for node in assigned:
            store = func(store, assignment[node])
        possible = [store]
    else:
        if len(unassigned) == 1: # just one unassigned
            a = unassigned.pop()
            possible = domain[a]
        else:
            possible = []
            a = unassigned.pop()
            b = unassigned.pop()
            for item1 in domain[a]:
                for item2 in domain[b]:
                    possible.append(func(item1, item2))
            while unassigned:
                tmp = unassigned.pop()
                tmp_possible = []
                for item1 in possible:
                    for item2 in tmp:
                        tmp_possible.append(func(item1,item2))
                possible = tmp_possible[:]

        for item in assigned:
            val = assignment[item]
            possible = [ func(i,val) for i in possible]


    if node_type == 'S' or node_type == 'P':
        lsd = set() # least significant digit
        for val in possible:
            if val % 10 == 0:
                continue
            lsd.add(val%10)
        return list(lsd)
    elif node_type == 'T' or node_type == 'H':
        msd = set() # most significant digit
        for val in possible:
            msd.add(val // (10**floor(log10(val))))
        return list(msd)


def forward_check(assignment, domain, node, node_type, edge):
    for adj in edge[node]:
        if node_type[adj] == 'T': 
            pass
        elif node_type[adj] == 'S':
            if assignment[node] % 2 == 0:
                domain[adj] = [x for x in domain[node] if x % 2 == 0]
            elif assignment[node] == 5:
                domain[adj] = [x for x in domain[node] if x % 5 == 0]
        elif node_type[adj] == 'C':
            pass
        elif node_type[adj] == 'H':
            pass
        
    # Here we propogate the constraint
    for adj in edge[node]:
        domain[adj] = constrainter(assignment, adj, domain, edge, node_type=node_type[adj])
    return


def backtrack(assignment, node_type, domain, edge, mode):
    if valid(assignment, node_type, edge): 
        return assignment
    n = select_node(assignment, domain, mode=mode[0])
    for val in domain[n]:
        tmp_assignment = assignment[:]
        tmp_assignment[n] = val
        if consistent(tmp_assignment, n, node_type, edge):
            assignment[n] = val
            if mode[1] == '1':
                forward_check(assignment, domain, node=n, node_type=node_type, edge=edge)
            result = backtrack(assignment[:], node_type, domain[:], edge, mode)
            if result:
                return result
    return None


def AC3(assignment, node, domain, edge, node_type):
    pass



def initialize_list(node_num):
    l = []
    for i in range(node_num):
        l.append([])
    return l


def main():
    mode = "110"
    number_of_nodes = int(input())
    assignment = [None] * number_of_nodes

    edge_num = int(input())

    raw_node_type = input()
    node_type = raw_node_type.split(' ')

    edge = initialize_list(number_of_nodes)
    for _ in range(edge_num):
        e = list(map(int,input().split(' ')))
        edge[e[0]].append(e[1])
        edge[e[1]].append(e[0])

    domain = []
    for i in range(number_of_nodes):
        domain.append(list(range(1,10))) # Each node domain could be from 1 up to 9

    solution = backtrack(assignment[:], node_type, domain, edge, mode)
    print(solution)


if __name__ == "__main__":
    main()