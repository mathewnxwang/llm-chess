import chess
import chess.engine
import chess.pgn
import io

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
    weak_engine = ChessEngine(skill_level=1)
    board = chess.Board()

    game = chess.pgn.Game()
    node = game
    
    while not board.is_game_over():
        
        if board.turn == chess.WHITE:
            move = engine.get_best_move(board)
            board.push(move)
            print(f"Engine's move: {move}")

        else:
            move = weak_engine.get_best_move(board)
            board.push(move)
            print(f"Weak engine's move: {move}")
            # engine.get_and_execute_user_move(board)

        node = node.add_variation(board.move_stack[-1])

        print(board)
    
    engine.close()
    weak_engine.close()

    print("Game over.")
    print(board.result())

    game.headers["Result"] = board.result()

    pgn_string = io.StringIO()
    exporter = chess.pgn.FileExporter(pgn_string)
    game.accept(exporter)

    print("Game PGN:")
    print(pgn_string.getvalue())