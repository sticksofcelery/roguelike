from flask import Flask, render_template, jsonify, request, send_from_directory
from game.engine.game_state import GameState
from game.editor.routes import editor_bp
import os

app = Flask(__name__)
app.register_blueprint(editor_bp)  # Register the editor blueprint

game = GameState()


@app.route('/')
def index():
    return render_template('game.html')


@app.route('/game_state')
def get_game_state():
    return jsonify(game.to_dict())


@app.route('/move', methods=['POST'])
def move_player():
    data = request.json
    target_x = data.get('x')
    target_y = data.get('y')

    if target_x is None or target_y is None:
        return jsonify({'error': 'Invalid coordinates'}), 400

    game.try_move_player(target_x, target_y)
    return jsonify(game.to_dict())


@app.route('/reset', methods=['POST'])
def reset_level():
    game.initialize_level()  # Reset the current level
    return jsonify(game.to_dict())


@app.route('/music/<filename>')
def serve_music(filename):
    try:
        return send_from_directory('static/assets/music', filename)
    except Exception as e:
        print(f"Error serving music file: {e}")
        return str(e), 404


if __name__ == '__main__':
    # Ensure the template directory is correctly set
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.template_folder = template_dir
    app.run(debug=True)