from flask import Flask, send_file, request
import game  # Assuming game.py contains the game logic

app = Flask(__name__)

# Route to serve the HTML file
@app.route('/')
def index():
    return send_file('index .html')

# Route to handle commands from the HTML interface
@app.route('/run', methods=['POST'])
def run_command():
    data = request.get_json()
    command = data.get('command')

    # Handle the game commands by using functions from game.py
    if command == "start":
        response = "Game started! Welcome to the adventure."
    elif command == "look":
        response = "You are standing in a dense forest. Paths lead north, south, east, and west."
    elif command == "inventory":
        response = "You have a rusty sword, a small pouch of gold, and a map of the forest."
    elif command.startswith("go "):
        direction = command.split(" ")[1]
        if direction in ["north", "south", "east", "west"]:
            response = f"You head {direction}. The path is narrow and winding."
        else:
            response = "Invalid direction. You can go north, south, east, or west."
    elif command == "take sword":
        response = "You pick up the rusty sword. It feels heavy in your hand."
    elif command == "attack":
        response = "You swing your sword wildly. There is nothing here to attack."
    else:
        # This assumes that game.py has a function called 'process_command'
        # which takes the command and returns an appropriate response.
        try:
            response = game.process_command(command)
        except AttributeError:
            response = f"Unknown command: {command}"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)