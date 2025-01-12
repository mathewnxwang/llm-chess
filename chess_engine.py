import chess
import chess.engine

class ChessEngine:

    def __init__(self, skill_level: int):

        if skill_level < 0 or skill_level > 20:
            raise ValueError("Skill level must be between 0 and 20")

        stockfish_path = r"C:\Users\mnw47\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.engine.configure({"Skill Level": skill_level})

    def get_best_move(self, board, time_limit=0.1):
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        return result.move

    def get_and_execute_user_move(self, board: chess.Board) -> None:

        while True:

            move_str = input("Enter your move: ")

            try:
                move: chess.Move = board.parse_san(move_str)
                break
            except chess.InvalidMoveError:
                print("Invalid move notation. Try again.")
                continue
            except chess.IllegalMoveError:
                print("Illegal move. Try again.")
                continue
            except chess.AmbiguousMoveError:
                print("Ambiguous move. Try again.")
                continue

        board.push(move)

    def close(self):
        self.engine.quit()

if __name__ == "__main__":
    engine = ChessEngine(skill_level=10)
    board = chess.Board()
    
    while not board.is_game_over():
        
        if board.turn == chess.WHITE:
            move = engine.get_best_move(board)
            board.push(move)
            print(f"Engine's move: {move}")

        else:
            engine.get_and_execute_user_move(board)

        print(board)
    
    engine.close()

    print("Game over.")
    print(board.result())