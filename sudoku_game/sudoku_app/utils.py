def flatten_board(board):
    flattened_string = ""
    for row in board:
        for cell in row:
            if cell == None:
                cell = '0'
            flattened_string += str(cell)
    return flattened_string

def is_valid_solution(solution):
    solution = [solution[i:i+9] for i in range(0,81,9)]


    for row in solution:
        if not check_row(row):
            return False
    
    for col in range(9):
        if not check_column(solution,col):
            return False
        
    for region in range (9):
        if not check_region(solution,region):
            return False
    
    return True

def check_row(arr):
    return get_state(arr)

def check_column(arr, col_index):
    column = [arr[row][col_index] for row in range(9)]
    return get_state(column)

def check_region(arr, region_index):
    region = []
    row_start = (region_index // 3) * 3
    col_start = (region_index % 3) * 3
    for i in range(3):
        for j in range(3):
            region.append(arr[row_start + i][col_start + j])
    return get_state(region)
    
def get_state(arr):
    seen = []
    for i in arr:
        if i in seen:
            return 0
        else:
            seen.append(i)
    return seen[-1] if seen else None