from copy import deepcopy

PHASE = 6
PHASE_SIZE = 4
DIRECTION = {"clockwise", "anticlockwise"}
cube = [] 

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

def goal_test(node):
    if cube[0] == [1,1,1,1] and \
        cube[1] == [2,2,2,2] and \
        cube[2] == [3,3,3,3] and \
        cube[3] == [4,4,4,4] and \
        cube[4] == [5,5,5,5] and \
        cube[5] == [6,6,6,6]:
        return True
    return False


def depth_limited_search_decorator(initial_node):
    limit = 0
    while True:
        result = depth_limited_search(initial_node, limit)
        if result == "success": 
            break
    return result

def swap(a:int,b:int,c:int,d:int,direction:str):
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


def rotate(phase, direction):
    cp_cube = deepcopy(cube)
    if phase == 0:
        swap(0, 1, 2, 3, direction)
        swap(4, 8,12, 20, direction)
        swap(5, 9, 13, 21, direction)
    elif phase == 1:
        swap(4, 5, 6, 7, direction)
        swap(0, 8, 16, 20, direction)
        swap(2, 11, 19, 23, direction)
    elif phase == 2:
        swap(8, 9, 10, 11, direction)
        swap(16, 5, 3, 15, direction)
        swap(17, 6, 2, 12, direction)
    elif phase == 3:
        swap(12, 13, 14, 15, direction)
        swap(9, 1, 21, 17, direction)
        swap(10, 3, 18, 22, direction)
    elif phase == 4:
        swap(16, 17, 18, 19, direction)
        swap(11, 15, 21, 5, direction)
        swap(10, 14, 20, 6, direction)
    elif phase == 5:
        swap(20, 21, 22, 23, direction)
        swap(19, 14, 1, 7, direction)
        swap(18, 13, 0, 4, direction)

def depth_limited_search(node, limit):
    if goal_test(node): #TODO: should be implemented
        pass
    elif limit == 0: #TODO: should be implemented
        pass 
    else:
        for phase in range(PHASE): # We have 12 rotations in a rubik's cube
            for direction in DIRECTION:
                child = rotate(phase, direction) # TODO: To be implemented 
                result = depth_limited_search(child, limit-1)
                if result == cutoff:
                    cutoff = True
                elif result != failure:
                    return result
            if cutoff:
                return cutoff
            else:
                return failure


def main():
    print("Enter your cube:")
    for i in range(PHASE):
        tmp = input(f"[{i+1}]:").split(',')
        for j,k in zip(tmp, range(PHASE_SIZE)):
            cube.insert(i * PHASE + k, j)
    print(cube)

if __name__ == "__main__":
    main()