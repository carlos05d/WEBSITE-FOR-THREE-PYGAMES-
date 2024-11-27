from flask import Flask, render_template, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to run a specific game and 
# display its output
@app.route('/run_game/<game_name>')
def run_game(game_name):
    # Ensure case-insensitivity by normalizing the file name
    game_name = game_name.upper()
    game_path = os.path.join('games', game_name)
    
    # Check if the game file exists
    if os.path.exists(game_path):
        try:
            # Execute the game script and capture its output
            result = subprocess.run(
                ['python', game_path], text=True, capture_output=True
            )
            output = result.stdout if result.returncode == 0 else result.stderr
            return render_template('game_output.html', game_name=game_name, output=output)
        except Exception as e:
            return f"<p>Error running the game: {str(e)}</p>", 500
    else:
        return f"<p>Game '{game_name}' not found.</p>", 404


if __name__ == "__main__":
    app.run(debug=True)
