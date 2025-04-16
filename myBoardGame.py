from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
events_file = "events.txt"
board = [""] * 9
current_player = "X"

def load_game():
    global board, current_player
    if not os.path.exists(events_file):
        return
    with open(events_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Turn:"):
                current_player = line.strip().split(":")[1].strip()
            elif ":" in line:
                pos, symbol = line.strip().split(":")
                board[int(pos)] = symbol.strip()

def save_game():
    with open(events_file, "w") as f:
        f.write(f"Turn: {current_player}\n")
        for i in range(9):
            if board[i]:
                f.write(f"{i}: {board[i]}\n")

@app.route("/")
def index():
    return render_template("game.html", board=board, current_player=current_player)

@app.route("/move/<int:cell>")
def move(cell):
    global current_player
    if board[cell] == "":
        board[cell] = current_player
        current_player = "O" if current_player == "X" else "X"
        save_game()
    return redirect("/")

@app.route("/reset")
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    save_game()
    return redirect("/")

if __name__ == "__main__":
    load_game()
    app.run(debug=True)
