#!/usr/bin/env python3

import argparse
import random
import sys
import time
import os

# Constants
PLAYER = "X"
COMPUTER = "O"
EMPTY = " "

# Colors
class colors:
    RESET = '''\033[0m'''
    RED = '''\033[91m'''
    GREEN = '''\033[92m'''
    YELLOW = '''\033[93m'''
    BLUE = '''\033[94m'''
    PURPLE = '''\033[95m'''
    CYAN = '''\033[96m'''
    BOLD = '''\033[1m'''
    UNDERLINE = '''\033[4m'''

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    """Prints the game title with animation."""
    title = [
        "  _______ _        _______           _______         ",
        " |__   __(_)      |__   __|         |__   __|        ",
        "    | |   _  ___     | | __ _  ___     | | ___   ___  ",
        "    | |  | |/ __|    | |/ _` |/ __|    | |/ _ \ / _ \ ",
        "    | |  | | (__     | | (_| | (__     | | (_) |  __/ ",
        "    |_|  |_|\___|    |_|\__,_|\___|    |_|\___/ \___| "
    ]
    clear_screen()
    for line in title:
        print(f"{colors.CYAN}{line}{colors.RESET}")
        time.sleep(0.1)
    print(f"\n{colors.YELLOW}=================================================={colors.RESET}\n")

def print_board(board, winning_line=None):
    """Prints the Tic Tac Toe board with colors and highlights the winning line."""
    print()
    for i in range(3):
        row_str = []
        for j in range(3):
            idx = i * 3 + j
            char = board[idx]
            
            is_win_cell = winning_line and idx in winning_line
            
            if is_win_cell:
                # Highlight winning cells
                row_str.append(f"{colors.BOLD}{colors.GREEN}{char}{colors.RESET}")
            elif char == PLAYER:
                row_str.append(f"{colors.BLUE}{char}{colors.RESET}")
            elif char == COMPUTER:
                row_str.append(f"{colors.RED}{char}{colors.RESET}")
            else:
                row_str.append(f"{colors.BOLD}{char}{colors.RESET}")
        
        print(" " * 10 + f" {row_str[0]} | {row_str[1]} | {row_str[2]} ")
        if i < 2:
            print(" " * 10 + "---|---|---")
    print()

def check_win(board, player):
    """Checks if the given player has won and returns the winning line."""
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return condition
    return None

def check_draw(board):
    """Checks if the game is a draw."""
    return EMPTY not in board

def get_player_move(board):
    """Gets a valid move from the player."""
    while True:
        try:
            move_input = input(f"{colors.BLUE}Enter your move (1-9): {colors.RESET}")
            if not move_input:
                continue
            move = int(move_input) - 1
            if 0 <= move <= 8 and board[move] == EMPTY:
                return move
            else:
                print(f"{colors.YELLOW}Invalid move. Please choose an empty spot (1-9).{colors.RESET}")
        except ValueError:
            print(f"{colors.YELLOW}Invalid input. Please enter a number (1-9).{colors.RESET}")

def get_computer_move(board, difficulty):
    """Determines the computer's move based on difficulty."""
    available_moves = [i for i, spot in enumerate(board) if spot == EMPTY]

    if not available_moves:
        return None

    if difficulty == "easy":
        return random.choice(available_moves)

    elif difficulty == "normal":
        # Check if computer can win
        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = COMPUTER
            if check_win(temp_board, COMPUTER) is not None:
                return move

        # Check if player can win and block
        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = PLAYER
            if check_win(temp_board, PLAYER) is not None:
                return move

        # Try to take the center
        if 4 in available_moves:
            return 4

        # Otherwise, make a random move
        return random.choice(available_moves)

    elif difficulty == "hard":
        # Minimax algorithm for hard difficulty
        best_score = -float('inf')
        best_move = None

        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = COMPUTER
            score = minimax(temp_board, 0, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

def minimax(board, depth, is_maximizing):
    if check_win(board, COMPUTER) is not None:
        return 1
    if check_win(board, PLAYER) is not None:
        return -1
    if check_draw(board):
        return 0

    available_moves = [i for i, spot in enumerate(board) if spot == EMPTY]

    if is_maximizing:
        best_score = -float('inf')
        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = COMPUTER
            score = minimax(temp_board, depth + 1, False)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in available_moves:
            temp_board = list(board)
            temp_board[move] = PLAYER
            score = minimax(temp_board, depth + 1, True)
            best_score = min(score, best_score)
        return best_score

def main():
    """Main function to run the game."""
    parser = argparse.ArgumentParser(description="A command-line Tic Tac Toe game.")
    parser.add_argument("--easy", action="store_true", help="Easy difficulty")
    parser.add_argument("--normal", action="store_true", help="Normal difficulty")
    parser.add_argument("--hard", action="store_true", help="Hard difficulty")
    args = parser.parse_args()

    difficulty = "normal"
    if args.easy:
        difficulty = "easy"
    elif args.hard:
        difficulty = "hard"

    board = [EMPTY] * 9
    current_player = PLAYER

    print_title()
    print(f"{colors.CYAN}Welcome to Tic Tac Toe!{colors.RESET}")
    print(f"{colors.BLUE}You are {PLAYER}{colors.RESET} and {colors.RED}the computer is {COMPUTER}{colors.RESET}. Difficulty: {difficulty.capitalize()}")
    input(f"{colors.PURPLE}Press Enter to start...{colors.RESET}")

    while True:
        clear_screen()
        print_board(board)

        if current_player == PLAYER:
            move = get_player_move(board)
            board[move] = PLAYER
        else:
            print(f"{colors.RED}Computer is thinking...{colors.RESET}", end='', flush=True)
            for _ in range(3):
                time.sleep(0.2)
                print(".", end='', flush=True)
            time.sleep(0.4)
            
            move = get_computer_move(board, difficulty)
            if move is not None:
                board[move] = COMPUTER

        winning_line = check_win(board, current_player)
        if winning_line:
            clear_screen()
            print_board(board, winning_line=winning_line)
            if current_player == PLAYER:
                print(f"{colors.GREEN}{colors.BOLD}Congratulations! You win!{colors.RESET}")
            else:
                print(f"{colors.RED}{colors.BOLD}Computer wins! Better luck next time.{colors.RESET}")
            break
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print(f"{colors.YELLOW}{colors.BOLD}It's a draw!{colors.RESET}")
            break

        current_player = COMPUTER if current_player == PLAYER else PLAYER

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Goodbye.")
        sys.exit(0)