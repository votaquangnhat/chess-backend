from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import chess
import chess.engine
import minimax_alphabeta
import mcts
import time
import requests
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
game = chess.Board()


def evaluation(game):
    result = check_game_status()
    if not result:
        data = {'fen': game.fen()}
        url = "https://chess-api.com/v1"  # The API endpoint
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            d = response.json()
            if 'eval' in d:
                return d['eval']  # Print the value of 'eval' key if it exists
            else:
                return 'error from API'
        else:
            return 'error' + data['fen']
    else:
        return result

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
    promotion = data['promotion']

    try:
        move = chess.Move.from_uci(from_square + to_square + promotion)
        if move in game.legal_moves:
            game.push(move)
            result = check_game_status()
            if result:
                emit('announcement', {'result': result}, broadcast=True)
            
            score = 1#evaluation(game)
            emit('update', {'fen': game.fen(),
                            'turn': 'white' if game.turn else 'black',
                            'message': ('black' if game.turn else 'white') + ':' + from_square + to_square + promotion + f' score:{score}'},
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
    param = data['depth']
    
    if (game.turn and turn == 'white') or (not game.turn and turn == 'black'):
        
        move = None
        start_time = time.time()
        if mode == "Minimax":
            move = minimax_alphabeta.findMoveMinimax(board=game, depth=param)[1]
        elif mode == "AlphaBeta":
            move = minimax_alphabeta.findMoveAlphaBeta(board=game, depth=param, alpha=-float('inf'), beta=float('inf'))[1]
        elif mode == "MCTS":
            move = mcts.mcts_findNextMove(game=game, iteration=param)
        elif mode == "MCTS_NN":
            pass

        try:
            if move in game.legal_moves:
                execution_time = time.time() - start_time
                game.push(move)
                result = check_game_status()
                if result:
                    emit('announcement', {'result': result}, broadcast=True)
                
                score = 1#evaluation(game)
                emit('update', {'fen': game.fen(),
                                'turn': 'white' if game.turn else 'black',
                                'message': ('black' if game.turn else 'white') + ':' + chess.Move.uci(move) + f' (mode: {mode}({param}), score: {score}, time: {execution_time})'},
                    broadcast=True)
            else:
                emit('error', {'message': 'Illegal move'}, broadcast=True)
        except Exception as e:
            emit('error', {'message': str(e) + 'loi o day'}, broadcast=True)

@socketio.on('reset')
def handle_reset():
    global game
    game.reset()
    emit('update', {'fen': game.fen(), 'turn': 'white'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)