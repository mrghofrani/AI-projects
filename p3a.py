cube = list()


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

def depth_limited_search(node, limit):
    if goal_test(node): #TODO: should be implemented
        pass
    elif limit == 0: #TODO: should be implemented
        pass 
    else:
        for i in range(12): # We have 12 rotations in a rubik's cube
            child = rotate() # TODO: To be implemented 
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
    pass

if name == "__name__":
    pass