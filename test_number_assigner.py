import unittest
from number_assigner import valid

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
        
if __name__ == "__main__":
    unittest.main()
