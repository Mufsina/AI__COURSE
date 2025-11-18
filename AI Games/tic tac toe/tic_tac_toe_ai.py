import tkinter as tk
from tkinter import messagebox
import math
import random


def check_winner(board, player):
    win_combos = [(0,1,2), (3,4,5), (6,7,8),
                  (0,3,6), (1,4,7), (2,5,8),
                  (0,4,8), (2,4,6)]
    return any(board[i] == board[j] == board[k] == player for i,j,k in win_combos)

def is_draw(board):
    return ' ' not in board

def minimax(board, is_max):
    if check_winner(board, 'O'):
        return 1
    elif check_winner(board, 'X'):
        return -1
    elif is_draw(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                val = minimax(board, False)
                board[i] = ' '
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                val = minimax(board, True)
                board[i] = ' '
                best = min(best, val)
        return best

def best_move(board):
    best_score = -math.inf
    moves = []
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                moves = [i]
            elif score == best_score:
                moves.append(i)
    return random.choice(moves) 

# --- GUI PART ---
def on_click(i):
    global board
    if board[i] != ' ':
        return
    board[i] = 'X'
    buttons[i].config(text='X', state='disabled', disabledforeground='blue')

    if check_winner(board, 'X'):
        messagebox.showinfo("Game Over", "You win! ")
        reset_board()
        return
    if is_draw(board):
        messagebox.showinfo("Game Over", "It's a draw! ")
        reset_board()
        return

    ai = best_move(board)
    board[ai] = 'O'
    buttons[ai].config(text='O', state='disabled', disabledforeground='red')

    if check_winner(board, 'O'):
        messagebox.showinfo("Game Over", "AI wins! ")
        reset_board()
    elif is_draw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_board()

def reset_board():
    global board
    board = [' '] * 9
    for b in buttons:
        b.config(text=' ', state='normal')

# --- Tkinter Setup ---
root = tk.Tk()
root.title("Tic Tac Toe AI")

board = [' '] * 9
buttons = []

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    b = tk.Button(frame, text=' ', font=('Helvetica', 24), width=5, height=2,
                  command=lambda i=i: on_click(i))
    b.grid(row=i//3, column=i%3)
    buttons.append(b)

reset_button = tk.Button(root, text="Reset Game", font=('Helvetica', 14), command=reset_board)
reset_button.pack(pady=10)

root.mainloop()