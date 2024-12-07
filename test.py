import random
import chess
import mcts

if __name__ == '__main__':
    board = chess.Board()
    no_progress_moves = 0  # Counter for moves without progress

    while True:
        if no_progress_moves >= 50:  # Check for 50-move rule
            print("Stalemate due to 50 moves with out progress.")
            break

        next_move = mcts.mcts_findNextMove(board, 3)
        print(next_move)
        
        if next_move is None:
            break

        # Check for capture or pawn move
        if board.is_capture(next_move) or board.piece_at(next_move.from_square).piece_type == chess.PAWN:
            no_progress_moves = 0  # Reset counter
        else:
            no_progress_moves += 1  # Increment counter

        board.push(next_move)
        print(board)
        print()
    
    result = board.result()
    if result == '1-0':
        print('White wins')
    if result == '0-1':
        print('Black wins')
    if result == '1/2-1/2':
        print('Stalemate')