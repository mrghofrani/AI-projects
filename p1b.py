from itertools import permutations
PHASE = 6
PHASE_SIZE = 4
DIRECTION = {"clockwise", "anticlockwise"}

# My rubik's cube internal indexing is
#                +-------+
#                | 0   1 |
#                | 3   2 |
#         +------+-------+-------+
#         | 4  5 | 8   9 | 12 13 |
#         | 7  6 | 11 10 | 15 14 | 
#         +------+-------+-------+
#                | 16 17 |
#                | 19 18 |
#                +-------+
#                | 20 21 |
#                | 23 22 |
#                +-------+


class Node:
    def __init__(self, cube_arg, parent=None, phase=None, direction=None):
        self.cube = cube_arg
        self.parent = parent
        self.phase = phase
        self.direction = direction

    def __eq__(self, other):
        if isinstance(other, Node):
            return list(map(int, self.cube)) == list(map(int, other.cube))
        return False


def find_solution(fnode, bnode):
    solution_part1 = []
    while fnode.parent:
        solution_part1.append((fnode.phase + 1, fnode.direction))
        fnode = fnode.parent

    solution_part2 = []
    while bnode.parent:
        reverse_rotate = list(set(DIRECTION) - set(bnode.direction))[0]
        solution_part2.append((bnode.phase + 1, reverse_rotate))
        bnode = bnode.parent

    return solution_part1[::-1] + solution_part2


def print_node(node):
    cube = node.cube
    print("       +------+")
    print(f"       | {cube[0]}  {cube[1]} |")
    print(f"       | {cube[3]}  {cube[2]} |")
    print("+------+------+------+")
    print(f"| {cube[4]}  {cube[5]} | {cube[8]}  {cube[9]} | {cube[12]}  {cube[13]} |")
    print(f"| {cube[7]}  {cube[6]} | {cube[11]}  {cube[10]} | {cube[15]}  {cube[14]} |")
    print("+------+------+------+")
    print(f"       | {cube[16]}  {cube[17]} |")
    print(f"       | {cube[19]}  {cube[18]} |")
    print("       +------+")
    print(f"       | {cube[20]}  {cube[21]} |")
    print(f"       | {cube[23]}  {cube[22]} |")
    print("       +------+")


def swap(cube, a:int,b:int,c:int,d:int,direction:str):
    tmp = cube[a]
    if direction == "anticlockwise":
        cube[a] = cube[b]
        cube[b] = cube[c]
        cube[c] = cube[d]
        cube[d] = tmp
    elif direction == "clockwise":
        cube[a] = cube[d]
        cube[d] = cube[c]
        cube[c] = cube[b]
        cube[b] = tmp
    return cube


def rotate(node, phase, direction):
    cube = node.cube[:]
    if phase == 0:
        tmp_cube = swap(cube, 0, 1, 2, 3, direction)
        tmp_cube = swap(tmp_cube, 4, 8, 12, 22, direction)
        tmp_cube = swap(tmp_cube, 5, 9, 13, 23, direction)
    elif phase == 1:
        tmp_cube = swap(cube, 4, 5, 6, 7, direction)
        tmp_cube = swap(tmp_cube, 0, 8, 16, 20, direction)
        tmp_cube = swap(tmp_cube, 3, 11, 19, 23, direction)
    elif phase == 2:
        tmp_cube = swap(cube, 8, 9, 10, 11, direction)
        tmp_cube = swap(tmp_cube, 16, 5, 2, 15, direction)
        tmp_cube = swap(tmp_cube, 17, 6, 3, 12, direction)
    elif phase == 3:
        tmp_cube = swap(cube, 12, 13, 14, 15, direction)
        tmp_cube = swap(tmp_cube, 9, 1, 21, 17, direction)
        tmp_cube = swap(tmp_cube, 10, 2, 22, 18, direction)
    elif phase == 4:
        tmp_cube = swap(cube, 16, 17, 18, 19, direction)
        tmp_cube = swap(tmp_cube, 11, 15, 21, 7, direction)
        tmp_cube = swap(tmp_cube, 10, 14, 20, 6, direction)
    elif phase == 5:
        tmp_cube = swap(cube, 20, 21, 22, 23, direction)
        tmp_cube = swap(tmp_cube, 19, 14, 1, 4, direction)
        tmp_cube = swap(tmp_cube, 7, 18, 13, 0, direction)
    return Node(tmp_cube, parent=node, phase=phase, direction=direction)


def initialize_qb():
    colors = list(x+1 for x in range(PHASE))
    coloring_set = list(permutations(colors))
    qb = []
    for coloring in coloring_set:
        cube = []
        for i in range(PHASE):
            for k in range(PHASE_SIZE):
                cube.insert(i * PHASE_SIZE + k, coloring[i])
        qb.append(Node(cube))
    return qb


def exist(node, explored):
    for element in explored:
        if node.cube == element.cube:
            return True
    return False


def bidirectional_search(snode):
    qf = [snode] # queue of forward 
    ef = [snode] # explored set of forward 
    qb = initialize_qb() # queue of backward]
    eb = initialize_qb() # explored set of backward
    while qb and qf:
        if qf:
            node = qf.pop(0)
            if node in eb:
                matching_node = eb[eb.index(node)]
                solution = find_solution(node, matching_node) 
                return solution
            for phase in range(PHASE):
                for direction in DIRECTION:
                    child = rotate(node, phase, direction)
                    if not exist(child, ef):
                        ef.append(child)
                        qf.append(child)

        if qb:
            node = qb.pop(0)
            if node in ef:
                matching_node = ef[ef.index(node)]
                solution = find_solution(matching_node, node)
                return solution
            for phase in range(PHASE):
                for direction in DIRECTION:
                    child = rotate(node, phase, direction)
                    if not exist(child, eb):
                        eb.append(child)
                        qb.append(child)
        
    return None

def main():
    cube = []
    print("Enter your cube:")
    for i in range(PHASE):
        tmp = input(f"[{i+1}]:").split(',')
        for j,k in zip(tmp, range(PHASE_SIZE)):
            cube.insert(i * PHASE_SIZE + k, j)
        cube[i * PHASE_SIZE + 2], cube[i * PHASE_SIZE + 3] = cube[i * PHASE_SIZE + 3], cube[i * PHASE_SIZE + 2]
    snode = Node(cube)
    solution = bidirectional_search(snode)
    print(solution)

if __name__ == "__main__":
    main()