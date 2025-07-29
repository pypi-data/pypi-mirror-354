import random

import chess
import gradio as gr
from gradio_chessboard import Chessboard


def random_move(fen: str) -> str:
    board = chess.Board(fen)
    moves = list(board.legal_moves)
    move = random.choice(moves)
    board.push(move)
    return board.fen()


with gr.Blocks() as demo:
    gr.Markdown("# Play Chess with Gradio Chessboard")
    gr.Markdown(
        "This is a demo of the Gradio Chessboard component. You can play chess on it or use it to edit the position."
    )
    chessboard = Chessboard(label="Board", game_mode=True)
    chessboard.move(random_move, chessboard, chessboard)


if __name__ == "__main__":
    demo.launch()
