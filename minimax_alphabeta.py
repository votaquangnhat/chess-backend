import random
import chess

#The higher the score, the better the piece
piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}

#The higher the score, the better the position of the piece
knight_scores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

bishop_scores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4],
]

rook_scores = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4],
]

queen_scores = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 1, 2, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1],
]

pawn_scores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

piece_position_scores = {"N": knight_scores,
                         "n": knight_scores[::-1],
                         "B": bishop_scores,
                         "b": bishop_scores[::-1],
                         "Q": queen_scores,
                         "q": queen_scores[::-1],
                         "R": rook_scores,
                         "r": rook_scores[::-1],
                         "P": pawn_scores,
                         "p": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0

# Score the board based on the position of the pieces. The higher the score, the better for white, otherwise
def scoreBoard(board):
    if board.is_checkmate():
        if board.turn:  # white to move
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif board.is_stalemate():
        return STALEMATE  # draw
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_position_score = 0
            if piece.piece_type != chess.KING:  # Exclude king for position scores
                row, col = divmod(square, 8)
                piece_position_score = piece_position_scores[piece.symbol()][row][col]
            
            if piece.color == chess.WHITE:
                score += (piece_score[piece.symbol()] + piece_position_score)
            else:
                score -= (piece_score[piece.symbol().upper()] + piece_position_score)
    return score


# Find the best move using the Minimax algorithm
def findMoveMinimax(board, depth):
    #if leaf node
    if depth == 0 or not list(board.legal_moves) or board.is_game_over():
        return [scoreBoard(board), None]
    
    valid_moves = list(board.legal_moves)

    random.shuffle(valid_moves)
    
    if board.turn:  # White's turn, maximize score
        max_score = -float('inf')
        best_move = None
        for move in valid_moves:
            board.push(move)
            score, _ = findMoveMinimax(board, depth - 1)
            if score > max_score:
                max_score = score
                best_move = move
            board.pop()
        return [max_score, best_move]
    
    else:  # Black's turn, minimize score
        min_score = float('inf')
        best_move = None
        for move in valid_moves:
            board.push(move)
            score, _ = findMoveMinimax(board, depth - 1)
            if score < min_score:
                min_score = score
                best_move = move
            board.pop()
        return [min_score, best_move]

# Find the best move using the Minimax algorithm with alpha-beta pruning
def findMoveAlphaBeta(board, depth, alpha, beta):
    #if leaf node
    if depth == 0 or not list(board.legal_moves) or board.is_game_over():
        return [scoreBoard(board), None]

    valid_moves = list(board.legal_moves)
    random.shuffle(valid_moves)
    
    if board.turn:  # White's turn, maximize score
        max_score = -float('inf')
        best_move = None
        for move in valid_moves:
            board.push(move) 
            score, _ = findMoveAlphaBeta(board, depth - 1, alpha, beta)
            if score > max_score:
                max_score = score
                best_move = move
            board.pop()
            alpha = max(alpha, score)
            if beta <= alpha:  # Prune branches
                break
        return [max_score, best_move]
    
    else:  # Black's turn, minimize score
        min_score = float('inf')
        best_move = None
        for move in valid_moves:
            board.push(move)
            score, _ = findMoveAlphaBeta(board, depth - 1, alpha, beta)
            if score < min_score:
                min_score = score
                best_move = move
            board.pop()
            beta = min(beta, score)
            if beta <= alpha:  # Prune branches
                break
        return [min_score, best_move]

# Test case
if __name__ == '__main__':
    board = chess.Board()
    no_progress_moves = 0  # Counter for moves without progress

    while True:
        if no_progress_moves >= 50:  # Check for 50-move rule
            print("Stalemate due to 50 moves with   out progress.")
            break

        if board.turn:
            next_move = findMoveAlphaBeta(board, 4, -float('inf'), float('inf'))[1]
        else:
            next_move = findMoveMinimax(board, 3)[1]
        
        if next_move is None:
            break

        # Check for capture or pawn move
        if board.is_capture(next_move) or board.piece_at(next_move.from_square).piece_type == chess.PAWN:
            no_progress_moves = 0  # Reset counter
        else:
            no_progress_moves += 1  # Increment counter

        board.push(next_move)
        print(scoreBoard(board))
        print(board)
        print()
    
    result = board.result()
    if result == '1-0':
        print('White wins')
    if result == '0-1':
        print('Black wins')
    if result == '1/2-1/2':
        print('Stalemate')