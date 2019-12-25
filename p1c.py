from copy import deepcopy
PHASE = 6
PHASE_SIZE = 4
HEURISTIC1_CONSTANT = 4
HEURISTIC2_CONSTANT = 2
HEURISTIC3_CONSTANT = 1
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

class Cube:
    def __init__(self, phase=None):
        self.h = 0
        self.g = 0
        self.cube = None
        self.phase = None
        self.direction = None
        self.internal = None

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


def heuristic(cube):
    cube = cube.internal
    h1 = 0
    h2 = 0
    h3 = 0
    for i in range(PHASE):
        if len(set(cube[i * PHASE_SIZE : (i + 1) * PHASE_SIZE])) == len(cube[i * PHASE_SIZE : (i + 1) * PHASE_SIZE]):
            h1 += HEURISTIC1_CONSTANT
    for i in range(PHASE):
        if (len(set(cube[i * PHASE_SIZE : (i + 1) * PHASE_SIZE])) + 1) == len(cube[i * PHASE_SIZE : (i + 1) * PHASE_SIZE]):
            h2 += HEURISTIC2_CONSTANT
    for i in range(PHASE):
        if (len(set(cube[i * PHASE_SIZE : (i + 1) * PHASE_SIZE])) + 2) == len(cube[i * PHASE_SIZE : (i + 1) * PHASE_SIZE]):
            h3 += HEURISTIC3_CONSTANT


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


def aStar(start, goal, grid):
    frontier = set()
    current = start
    frontier.add(current)
    while frontier:
        current = min(frontier, key=lambda o:o.G + o.H)
        if goal_test(frontier): #TODO: should be checked
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        frontier.remove(current)
        for phase in range(PHASE):
            for direction in DIRECTION:
                child = rotate(cube[:], phase, direction)
                if cube in frontier:  # Check if we have found a better way to reach child cube
                    new_g = current.G + 1
                    if node.G > new_g:
                        #If so, update the node to have a new parent
                        node.G = new_g
                        node.parent = current
                else:
                    #If it isn't in the open set, calculate the G and H score for the node
                    node.G = current.G + current.move_cost(node)
                    node.H = heuristic(node, goal)
                    #Set the parent to our current item
                    node.parent = current
                    #Add it to the set
                    openset.add(node)

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