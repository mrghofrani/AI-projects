from copy import deepcopy

PHASE = 6
PHASE_SIZE = 4
DIRECTION = {"clockwise", "anticlockwise"}
cube = [] 
solution = []

# My rubik's cube internal indexing is
#                +-------+
#                | 0   1 |
#                | 2   3 |
#         +------+-------+-------+
#         | 4  5 | 8   9 | 12 13 |
#         | 6  7 | 10 11 | 14 15 | 
#         +------+-------+-------+
#                | 16 17 |
#                | 18 19 |
#                +-------+
#                | 20 21 |
#                | 22 23 |
#                +-------+

def goal_test(cube):
    sorted = [False, False, False, False, False]
    for i in range(PHASE):
        side_is_sorted = True
        for j in range(i*PHASE, i*PHASE+PHASE_SIZE):
            if cube[j] != (i+1):
                side_is_sorted = False
                break
        sorted[i] = side_is_sorted
    
    for item in sorted:
        if not item:
            return False
    return True


def depth_limited_search_decorator(initial_node):
    limit = 0
    while True:
        result = depth_limited_search(initial_node, limit)
        if result == "success": 
            break
    return result

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
        tmp_cube = swap(tmp_cube, 4, 8,12, 20, direction)
        tmp_cube = swap(tmp_cube, 5, 9, 13, 21, direction)
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

def depth_limited_search(cube, limit, phase, direction):
    if goal_test(cube):
        solution.append((cube, phase, direction))
        return True
    elif limit == 0:
        return False 
    else:
        cutoff = False
        for phase in range(PHASE): # We have 12 rotations in a rubik's cube
            for direction in DIRECTION:
                child = rotate(cube, phase, direction) # TODO: To be implemented 
                result = depth_limited_search(child, limit-1, phase, direction)
                if result:
                    cutoff = True
                elif result:
                    solution.append((cube, phase, direction))
                    return True
        if cutoff:
            return False


def main():
    print("Enter your cube:")
    for i in range(PHASE):
        tmp = input(f"[{i+1}]:").split(',')
        for j,k in zip(tmp, range(PHASE_SIZE)):
            cube.insert(i * PHASE + k, j)
    print(cube)

if __name__ == "__main__":
    main()