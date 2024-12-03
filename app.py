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

@socketio.on('move')
def handle_move(data):
    global game
    from_square = data['from']
    to_square = data['to']
    try:
        move = chess.Move.from_uci(from_square + to_square)
        if move in game.legal_moves:
            game.push(move)
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
                print(move)
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