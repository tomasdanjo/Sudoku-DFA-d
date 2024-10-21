from django.db import models
from sudoku import Sudoku

# Create your models here.
class SudokuGame(models.Model):
    puzzle = models.CharField(max_length=81)
    solution = models.CharField(max_length=81)
    player_progress = models.CharField(max_length=81,blank=True,null=True)

    class Meta:
        app_label = 'sudoku_app' 

    def __str__(self):
        return f"Sudoku puzzle {self.id}"


    def generate_puzzle(self,difficulty=0.2):
        sudoku_puzzle = Sudoku(3).difficulty(difficulty)
        solved_puzzle = sudoku_puzzle.solve()

        # puzzle_generator = Sudoku(difficulty=difficulty)  # Create a Sudoku puzzle generator
        # puzzle, solution = puzzle_generator.generate()  # Generate a puzzle and its solution
        self.puzzle = self.flatten_board(sudoku_puzzle.board)
        self.solution = self.flatten_board(solved_puzzle    .board) # Store the solution as a string
        self.save()

    def flatten_board(self,board):
        flattened_string = ""
        for row in board:
            for cell in row:
                if cell == None:
                    cell = '0'
                flattened_string += str(cell)
        return flattened_string

    