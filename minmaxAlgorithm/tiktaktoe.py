def isMovesLeft(board):
    for row in board:
        if 0 in row:
            return True
    return False

def getMoves(board):
    moves = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:  
                moves.append((i, j))
    return moves

def evaluate(board):
    for row in board:
        if sum(row) == 3:
            return 10
        if sum(row) == -3:
            return -10

    for col in range(3):
        if sum(board[row][col] for row in range(3)) == 3: 
            return 10
        if sum(board[row][col] for row in range(3)) == -3:
            return -10

    if sum(board[i][i] for i in range(3)) == 3 or sum(board[i][2 - i] for i in range(3)) == 3:  # AI wins
        return 10
    if sum(board[i][i] for i in range(3)) == -3 or sum(board[i][2 - i] for i in range(3)) == -3:  # Opponent wins
        return -10

    return 0


def minimax(board, depth, isMaximizingPlayer, alpha, beta):
    score = evaluate(board)
    if score != 0: 
        return score
    
    if not isMovesLeft(board):
        return 0 
    
    if isMaximizingPlayer:
        best = -float('inf')
        for move in getMoves(board):
            board[move[0]][move[1]] = 1
            best = max(best, minimax(board, depth + 1, False, alpha, beta))
            board[move[0]][move[1]] = 0
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for move in getMoves(board):
            board[move[0]][move[1]] = -1 
            best = min(best, minimax(board, depth + 1, True, alpha, beta))
            board[move[0]][move[1]] = 0
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def print_board(board):
    symbols = {0: " ", 1: "X", -1: "O"}
    for row in board:
        print("|" + "|".join(symbols[cell] for cell in row) + "|")

def make_move(board, row, col, player):
    if board[row][col] == 0:
        board[row][col] = player
        return True
    return False

def get_user_move(board):
    while True:
        try:
            row, col = map(int, input("Enter your move (row col): ").split())
            if make_move(board, row, col, -1):
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter row and column as two numbers separated by a space.")

def find_best_move(board):
    best_val = -float('inf')
    best_move = (-1, -1)
    for move in getMoves(board):
        make_move(board, move[0], move[1], 1)  
        move_val = minimax(board, 0, False, -float('inf'), float('inf'))
        board[move[0]][move[1]] = 0  
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

def main():
    board = [[0, 0, 0] for _ in range(3)]
    player_turn = True  
    
    while isMovesLeft(board):
        print_board(board)
        if player_turn:
            get_user_move(board)
        else:
            print("AI is making a move...")
            row, col = find_best_move(board)
            make_move(board, row, col, 1)
            print(f"AI placed an 'X' in row {row}, column {col}.")
        player_turn = not player_turn
        if evaluate(board) == 10:
            print("AI wins!")
            break
        elif evaluate(board) == -10:
            print("User wins!")
            break
    else:  # If no moves left
        print("It's a tie!")
    print_board(board)

if __name__ == "__main__":
    main()
