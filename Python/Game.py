import Arc
import time
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    payload: Any=field(compare=False)

class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.revisions = 0
        self.vars = None

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        return self.ac3()


    def ac3(self):
        # Initialize the queue
        start = time.time()
        q = PriorityQueue()
        # q = []

        # def add_arc(x, y):
        #     q.append((x, y))

        for row in range(9):
            for col in range(9):
                x = self.sudoku.board[row][col]
                for y in x.get_neighbours():
                    self.add_arc(x, y, q)
        
        # While queue is not empty
        while not q.empty():
            # Get the first element of the queue
            # x, y = q.pop(0)
            item = q.get()
            x, y = item.payload
            if self.revise(x, y):
                if x.get_domain_size() == 0:
                    print(f"No domain found for field {x}")
                    return False
                for z in x.get_neighbours():
                    if z != y:
                        self.add_arc(z, x, q)
        finish = time.time()-start
        print(f'Time: {finish}s, Revisions: {self.revisions}')
        print(self.sudoku)
        return True
    
    def add_arc(self, x, y, q):
        # priority = (x.get_domain_size()) # Minimum domain values heuristic
        priority = sum([b.get_domain_size() for b in y.get_neighbours()]) # Heuristic for 
        payload = (x, y)
        wrapper = PrioritizedItem(priority, payload)
        q.put(wrapper)

    def revise(self, x, y):
        self.revisions += 1
        revised = False
        domain_x = x.get_domain()
        domain_y = y.get_domain()
        for elem in domain_x:
            if not any(elem != z for z in domain_y):
                x.remove_from_domain(elem)
                revised = True
        return revised
    
    def backtrack_search(self):
        start = time.time()
        board = self.backtracking(self.sudoku.board)
        finish = time.time() - start
        if board:
            print(self.sudoku)
            print(f'Time: {finish}s')
            return True
        else:
            print("Did not manage to solve")
            return False
    

    def backtracking(self, board):
        if self.valid_solution():
            return True
        
        var = self.select_unsigned_var(board)
        for number in var.get_domain():
            inferences = []
            if all([number != x.value for x in var.get_neighbours()]):
                var.value = number
                inferences = self.inferences(var, number)
                if inferences:
                    for k, n in inferences:
                        k.get_domain().remove(n)
                    result = self.backtracking(board)
                    if result:
                        return result
                    var.value = 0
                    for k, n in inferences:
                        k.get_domain().append(n)
        return False
                    


    def inferences(self, var, number):
        inferences = []
        for k in var.get_neighbours():
            if number in k.get_domain():
                inferences.append((k, number))
                if k.get_domain_size() == 1:
                    return None
        return inferences
    
    def select_unsigned_var(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col].value == 0:
                    return board[row][col]




    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        for split in self.sudoku.board:
            for elem in split:
                if elem.value == 0:
                    return False
                for neighbour in elem.neighbours:
                    if elem.value == neighbour.value:
                        return False
        return True
