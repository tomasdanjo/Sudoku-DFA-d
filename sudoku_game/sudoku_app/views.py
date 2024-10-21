from django.shortcuts import render, redirect,get_object_or_404
from .models import SudokuGame
from sudoku import Sudoku
from .utils import *

# Create your views here.
def landing_page(request):
    if request.method == 'POST':
        difficulty = 0.1    
        sudoku_puzzle = Sudoku(3).difficulty(difficulty)
        solved_puzzle = sudoku_puzzle.solve()
        # Save the puzzle to the database
        new_game = SudokuGame.objects.create(
            puzzle=flatten_board(sudoku_puzzle.board),
            solution=flatten_board(solved_puzzle.board),
            player_progress=flatten_board(sudoku_puzzle.board),
        )
        return redirect('sudoku_game', id=new_game.id)

    return render(request, 'landing_page.html',{} )

def success_page(request):
    game_id = request.session['game_id']
    print("Game ID retrieved from session:", game_id)
    status = request.session['status']  # Default message if not set

    if request.method == 'POST':
        difficulty = request.POST.get('difficulty')
        difficulty = float(difficulty)/100-0.001
        sudoku_puzzle = Sudoku(3).difficulty(difficulty)
        solved_puzzle = sudoku_puzzle.solve()
        new_game = SudokuGame.objects.create(
            puzzle=flatten_board(sudoku_puzzle.board),
            solution=flatten_board(solved_puzzle.board),
            player_progress=flatten_board(sudoku_puzzle.board),
        )
        return redirect('sudoku_game', id=new_game.id)
        
    return render(request, 'success.html', {
        'game_id': game_id,
        'status': status,
    })

def sudoku_game(request, id):
    if request.method == 'GET':
        sudoku_puzzle = get_object_or_404(SudokuGame,id=id)
        puzzle_data = sudoku_puzzle.puzzle
        progress_data = sudoku_puzzle.player_progress
        puzzle_original_list = [puzzle_data[i:i+9] for i in range(0, 81, 9)]
        puzzle_progress_list = [progress_data[i:i+9] for i in range(0, 81, 9)]



        combined = []

        for i in range(9):  # Assuming a 9x9 Sudoku
            row = []
            for j in range(9):
                # Store the original value and the progress value together
                if puzzle_original_list[i][j] == 0:
                    # If the original is 0, use the progress value in the format [0, progress_value]
                    row.append([0, puzzle_original_list[i][j]])
                else:
                    # Otherwise, use the original value and 0 to indicate it's not an input field
                    row.append([puzzle_original_list[i][j], puzzle_progress_list[i][j]])
            combined.append(row)
            
        context = {
            'puzzle': combined,  # Original pre-filled puzzle for read-only logic
            'game_id': id,
        }

        return render(request, 'game.html', context)

    elif request.method == 'POST':
        action = request.POST.get('action')
        game_id = request.POST.get('game_id')
        
        if action == 'Save Solution':
            player_progress = request.POST.getlist('progress[]')  # Assuming you send the progress as a list of inputs
            player_progress = ['0' if item =='' else item for item in player_progress]
            progress_str = ''.join(player_progress)  # Convert list of progress values into a string
            
            # Update the existing game record with the player's progress
            sudoku_game = SudokuGame.objects.get(id=game_id)
            sudoku_game.player_progress = progress_str
            sudoku_game.save()
            
            return redirect('sudoku_game', id=game_id)
        
        elif action == 'Submit Solution':
            player_progress = request.POST.getlist('progress[]')
            player_progress = ['0' if item =='' else item for item in player_progress]
            progress_str = ''.join(player_progress)  # Convert list of progress values into a string
            
            # Fetch the solution from the database
            sudoku_game = SudokuGame.objects.get(id=game_id)
            sudoku_game.player_progress = progress_str
            sudoku_game.save()

            correct_solution = sudoku_game.solution
            
            # Check if the player's progress matches the solution
            if is_valid_solution(progress_str):
                # Solution is correct
                request.session['game_id'] = game_id
                request.session['status'] = "Congratulations! You\'ve Completed the Puzzle!"
                print("Game ID set in session:", request.session['game_id'])


                return redirect('success_page')
            else:
                # Solution is incorrect
                sudoku_puzzle = get_object_or_404(SudokuGame,id=id)
                puzzle_data = sudoku_puzzle.puzzle
                progress_data = sudoku_puzzle.player_progress
                puzzle_original_list = [puzzle_data[i:i+9] for i in range(0, 81, 9)]
                puzzle_progress_list = [progress_data[i:i+9] for i in range(0, 81, 9)]



                combined = []

                for i in range(9):  # Assuming a 9x9 Sudoku
                    row = []
                    for j in range(9):
                        # Store the original value and the progress value together
                        if puzzle_original_list[i][j] == 0:
                            # If the original is 0, use the progress value in the format [0, progress_value]
                            row.append([0, puzzle_original_list[i][j]])
                        else:
                            # Otherwise, use the original value and 0 to indicate it's not an input field
                            row.append([puzzle_original_list[i][j], puzzle_progress_list[i][j]])
                    combined.append(row)
                return render(request, 'game.html', {
                    'game_id': game_id,
                    'puzzle':combined,
                    'error_message': 'The solution you provided is incorrect. Please try again.'
                })
