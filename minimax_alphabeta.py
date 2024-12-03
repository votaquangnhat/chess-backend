import random
import chess

#The higher the score, the better the piece
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

#The higher the score, the better the position of the piece
knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

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
    if depth == 0:
        return [scoreBoard(board), None]
    
    valid_moves = list(board.legal_moves)
    random.shuffle(valid_moves)
    
    if board.turn:  # White's turn, maximize score
        max_score = -CHECKMATE
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
        min_score = CHECKMATE
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
    if depth == 0:
        return [scoreBoard(board), None]

    valid_moves = list(board.legal_moves)
    random.shuffle(valid_moves)
    
    if board.turn:  # White's turn, maximize score
        max_score = -CHECKMATE
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
        min_score = CHECKMATE
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

    while(True):
        if board.turn:
            next_move = findMoveAlphaBeta(board, 4, -float('inf'), float('inf'))[1]   #white side use AlphaBeta algorithm
        else:
            next_move = findMoveMinimax(board, 3)[1]                                  #black side use Minimax algorithm
        
        if next_move is None:   #stalemate or checkmate
            break
        
        board.push(next_move)
        print(next_move)
        print(scoreBoard(board))
        print(board)
        print()
    
    if(board.is_checkmate()):
        print('Checkmate')
    else:
        print('Stalemate')