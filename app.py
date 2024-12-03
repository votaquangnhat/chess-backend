from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import chess
import minimax_alphabeta

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
game = chess.Board()

@app.route('/')
def index():
    return jsonify({'message': 'Chess game server is running'})

def check_game_status():
    """Check the game status and return the result."""
    if game.is_checkmate():
        return 'White wins!' if not game.turn else 'Black wins!'
    elif game.is_stalemate():
        return 'Stalemate'
    elif game.is_insufficient_material():
        return 'Draw (Insufficient Material)'
    elif game.is_fifty_moves():
        return 'Draw (50-move rule)'
    elif game.is_fivefold_repetition():
        return 'Draw (Fivefold Repetition)'
    return None

@socketio.on('move')
def handle_move(data):
    global game
    from_square = data['from']
    to_square = data['to']
    try:
        move = chess.Move.from_uci(from_square + to_square)
        if move in game.legal_moves:
            game.push(move)
            result = check_game_status()
            if result:
                emit('announcement', {'result': result}, broadcast=True)
            else:
                emit('update', {'fen': game.fen(),
                                'turn': 'white' if game.turn else 'black',
                                'message': ('black' if game.turn else 'white') + ':' + from_square + to_square},
                    broadcast=True)

        else:
            emit('error', {'message': 'Illegal move'}, broadcast=True)
    except Exception as e:
        emit('error', {'message': str(e)}, broadcast=True)

@socketio.on('ai_move')
def handle_ai_move(data):
    global game
    turn = data['turn']
    mode = data['mode']
    
    if (game.turn and turn == 'white') or (not game.turn and turn == 'black'):
        move_uci = None
        move = None
        if mode == "Minimax":
            move = minimax_alphabeta.findMoveMinimax(game, 3)[1]
        elif mode == "AlphaBeta":
            move = minimax_alphabeta.findMoveAlphaBeta(game, 4, -float('inf'), float('inf'))[1]
        elif move_uci == "MCTS":
            move_uci = None
        elif mode == "MCTS_NN":
            move_uci = None

        try:
            if move in game.legal_moves:
                game.push(move)
                result = check_game_status()
                if result:
                    emit('announcement', {'result': result}, broadcast=True)
                else:
                    emit('update', {'fen': game.fen(),
                                    'turn': 'white' if game.turn else 'black',
                                    'message': ('black' if game.turn else 'white') + ':' + chess.Move.uci(move)},
                        broadcast=True)
            else:
                emit('error', {'message': 'Illegal move'}, broadcast=True)
        except Exception as e:
            emit('error', {'message': str(e)}, broadcast=True)

@socketio.on('reset')
def handle_reset():
    global game
    game.reset()
    emit('update', {'fen': game.fen(), 'turn': 'white'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)