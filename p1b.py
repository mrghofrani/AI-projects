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
    def __init__(self, cube_arg, parent_arg=None, phase_arg=None, direction_arg=None):
        self.cube = cube_arg
        self.phase = phase_arg
        self.direction = direction_arg
        self.parent = parent_arg

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.cube == other.cube
        return False

def find_solution(node, from_start):
    backup = node
    solution_part1 = []
    while node.parent:
        solution_part1.append((node.phase + 1, node.direction))
        node = node.parent

    node = backup
    solution_part2 = []
    while node.parent:
        solution_part2.append((backup.phase + 1, backup.direction))
        node = node.parent

    if from_start:
        solution_part1 = solution_part1[::-1]
    else:
        solution_part2 = solution_part2[::-1]
    return solution_part1 + solution_part2

def print_cube(cube):
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

def goal_test(cube):
    sorted = [False, False, False, False, False, False]
    for i in range(PHASE):
        side_is_sorted = True
        norm = cube[i * PHASE_SIZE]
        for j in range(i * PHASE_SIZE, (i + 1) * PHASE_SIZE):
            if cube[j] != norm:
                side_is_sorted = False
                break
        sorted[i] = side_is_sorted
    
    for item in sorted:
        if not item:
            return False
    return True

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


def rotate(cube, phase, direction):
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
    return tmp_cube

def bidirectional_search(snode):
    qf = list() # queue of forward 
    ef = set() # explored set of forward 
    qb = list() # queue of backward
    eb = set() # explored set of backward
    while qb and qf:
        if qf:
            node = qf.pop(0)
            if goal_test(node) or node in qb:
                solution = find_solution(node) # TODO: Must be implemented
                return True
            for phase in range(PHASE):
                for direction in DIRECTION:
                    child = rotate(node, phase, direction)
                    if child not in ef:
                        ef.add(child)
                        qf.append(child)
        if qb:
            node = qb.pop(0)
            if node == snode or node in qf:
                solution = find_solution() # TODO: Must be implemented
                return True
            for phase in range(PHASE):
                for direction in DIRECTION:
                    child = rotate(node, phase, direction)
                    if child not in eb:
                        eb.add(child)
                        qb.append(child)

def main():
    cube = []
    print("Enter your cube:")
    for i in range(PHASE):
        tmp = input(f"[{i+1}]:").split(',')
        for j,k in zip(tmp, range(PHASE_SIZE)):
            cube.insert(i * PHASE_SIZE + k, j)
        cube[i * PHASE_SIZE + 2], cube[i * PHASE_SIZE + 3] = cube[i * PHASE_SIZE + 3], cube[i * PHASE_SIZE + 2]
    print_cube(cube)
    
    solution = []
    (_, solution) = depth_limited_search_decorator(cube, solution)
    print(solution)

if __name__ == "__main__":
    main()