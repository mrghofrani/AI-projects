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