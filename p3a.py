from copy import deepcopy

PHASE = 6
PHASE_SIZE = 4
DIRECTION = {"clockwise", "anticlockwise"}
cube = [] 
solution = []

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
        for j in range(i * PHASE_SIZE, (i + 1) * PHASE_SIZE):
            if int(cube[j]) != (i+1):
                side_is_sorted = False
                break
        sorted[i] = side_is_sorted
    
    for item in sorted:
        if not item:
            return False
    return True

def swap(cube, a:int,b:int,c:int,d:int,direction:str):
    tmp = cube[a]
    if direction == "clockwise":
        cube[a] = cube[b]
        cube[b] = cube[c]
        cube[c] = cube[d]
        cube[d] = tmp
    elif direction == "anticlockwise":
        cube[a] = cube[d]
        cube[d] = cube[c]
        cube[c] = cube[b]
        cube[b] = tmp
    return cube


def rotate(cube, phase, direction):
    if phase == 0:
        tmp_cube = swap(cube, 0, 1, 2, 3, direction)
        tmp_cube = swap(tmp_cube, 4, 8,12, 22, direction)
        tmp_cube = swap(tmp_cube, 5, 9, 13, 23, direction)
    elif phase == 1:
        tmp_cube = swap(cube, 4, 5, 6, 7, direction)
        tmp_cube = swap(tmp_cube, 0, 8, 16, 20, direction)
        tmp_cube = swap(tmp_cube, 2, 11, 19, 23, direction)
    elif phase == 2:
        tmp_cube = swap(cube, 8, 9, 10, 11, direction)
        tmp_cube = swap(tmp_cube, 16, 5, 3, 15, direction)
        tmp_cube = swap(tmp_cube, 17, 6, 2, 12, direction)
    elif phase == 3:
        tmp_cube = swap(cube, 12, 13, 14, 15, direction)
        tmp_cube = swap(tmp_cube, 9, 1, 21, 17, direction)
        tmp_cube = swap(tmp_cube, 10, 3, 18, 22, direction)
    elif phase == 4:
        tmp_cube = swap(cube, 16, 17, 18, 19, direction)
        tmp_cube = swap(tmp_cube, 11, 15, 21, 5, direction)
        tmp_cube = swap(tmp_cube, 10, 14, 20, 6, direction)
    elif phase == 5:
        tmp_cube = swap(cube, 20, 21, 22, 23, direction)
        tmp_cube = swap(tmp_cube, 19, 14, 1, 7, direction)
        tmp_cube = swap(tmp_cube, 18, 13, 0, 4, direction)
    return tmp_cube

def depth_limited_search(cube, limit, solution, phase, direction):
    if goal_test(cube):
        solution.append((phase+1, direction))
        return True, solution
    elif limit == 0:
        return False, []
    else:
        cutoff = False
        for phase in range(PHASE): # We have 12 rotations in a rubik's cube
            for direction in DIRECTION:
                print_cube(cube)
                child = rotate(cube, phase, direction) 
                print_cube(child)
                result = depth_limited_search(child, limit-1, solution, phase, direction)
                if result:
                    solution.append((phase+1, direction))
                    return True, solution
                else:
                    cutoff = False
        if cutoff:
            return False, []

def depth_limited_search_decorator(cube, solution):
    limit = 0
    while True:
        (result, solution) = depth_limited_search(cube, limit, solution, None, None)
        if result: 
            break
        limit += 1
    return result, solution

def main():
    print("Enter your cube:")
    for i in range(PHASE):
        tmp = input(f"[{i+1}]:").split(',')
        for j,k in zip(tmp, range(PHASE_SIZE)):
            cube.insert(i * PHASE_SIZE + k, j)
    
    solution = []
    (_, solution) = depth_limited_search_decorator(cube, solution)
    print(solution)

if __name__ == "__main__":
    main()