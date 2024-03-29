import unittest
from number_assigner import valid, backtrack

class TestNumberAssigner(unittest.TestCase):

    def test_valid_function(self):
        node_type = ['C', 'P', 'H', 'S', 'S', 'H', 'H', 'T', 'C']
        edge = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 6],
            6: [5, 7],
            7: [6, 8],
            8: [7]
        }
        assignment = [9,1,7,6,8,3,5,2,4]
        self.assertEqual(valid(assignment, node_type, edge), True)

        assigment = [9,1,7,6,8,3,5,3,4]
        self.assertEqual(valid(assigment, node_type, edge), False)

    
class TestCaseTester(unittest.TestCase):

    def test_case1(self):
        mode = "110"
        number_of_nodes = 3
        assignment = [None] * number_of_nodes
        node_type = ['C', 'T', 'C']
        edge = {
            0: [1],
            1: [0, 2], 
            2: [1]
        }

        domain = []
        for _ in range(number_of_nodes):
            domain.append(list(range(1,10))) # Each node domain could be from 1 up to 9

        solution = backtrack(assignment, node_type, domain, edge, mode)
        self.assertIsNotNone(solution, msg=f"solution was {solution}")

    def test_case2(self):
        mode = "110"
        number_of_nodes = 3
        assignment = [None] * number_of_nodes
        node_type = ['C', 'P', 'C']
        edge = {
            0: [1],
            1: [0, 2], 
            2: [1]
        }

        domain = []
        for _ in range(number_of_nodes):
            domain.append(list(range(1,10))) # Each node domain could be from 1 up to 9

        solution = backtrack(assignment, node_type, domain, edge, mode)
        self.assertIsNotNone(solution, msg=f"solution was {solution}")

    def test_case3(self):
        mode = "110"
        number_of_nodes = 3
        assignment = [None] * number_of_nodes
        node_type = ['C', 'H', 'C']
        edge = {
            0: [1],
            1: [0, 2], 
            2: [1]
        }

        domain = []
        for _ in range(number_of_nodes):
            domain.append(list(range(1,10))) # Each node domain could be from 1 up to 9

        solution = backtrack(assignment, node_type, domain, edge, mode)
        self.assertIsNotNone(solution, msg=f"solution was {solution}")
        
if __name__ == "__main__":
    unittest.main()
