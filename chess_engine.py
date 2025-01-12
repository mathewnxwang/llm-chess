import chess
import chess.engine
import chess.pgn
import io

from llm_manager import LLMManager

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

    def close(self):
        self.engine.quit()


def get_and_execute_user_move(board: chess.Board) -> None:

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


def get_and_execute_llm_move(llm_manager: LLMManager, board: chess.Board, position: str) -> None:

    retries = 3
    error_message = None
    while retries > 0:

        move_str = llm_manager.make_llm_move(position=position, error_message=error_message)

        try:
            move: chess.Move = board.parse_san(move_str)
            break
        except chess.InvalidMoveError:
            error_message = f"Invalid move notation: '{move_str}'."
            print(error_message)
            retries -= 1
            continue
        except chess.IllegalMoveError:
            error_message = f"Illegal move: '{move_str}'."
            print(error_message)
            retries -= 1
            continue
        except chess.AmbiguousMoveError:
            error_message = f"Ambiguous move: '{move_str}'."
            print(error_message)
            retries -= 1
            continue

    if retries == 0:
        raise Exception("Failed to get a valid LLM move after 3 attempts.")

    board.push(move)


def convert_board_to_pgn(board: chess.Board) -> str:
    pgn = chess.pgn.Game()
    pgn.setup(board)
    pgn_string = io.StringIO()
    exporter = chess.pgn.FileExporter(pgn_string)
    game.accept(exporter)

    print("PGN string for the LLM: \n" + pgn_string.getvalue())
    return pgn_string.getvalue()


if __name__ == "__main__":
    engine = ChessEngine(skill_level=10)
    board = chess.Board()
    llm_manager = LLMManager()

    game = chess.pgn.Game()
    node = game
    
    while not board.is_game_over():
        
        if board.turn == chess.WHITE:
            move = engine.get_best_move(board)
            board.push(move)
            print(f"Engine's move: {move}")

        else:
            # get_and_execute_user_move(board)
            position = convert_board_to_pgn(board)
            get_and_execute_llm_move(
                llm_manager=LLMManager(),
                board=board,
                position=position
            )

        node = node.add_variation(board.move_stack[-1])

        print(f"Current board: \n{board}\n")
    
    engine.close()

    print("Game over.")
    print(board.result())

    game.headers["Result"] = board.result()

    pgn_string = io.StringIO()
    exporter = chess.pgn.FileExporter(pgn_string)
    game.accept(exporter)

    print("Game PGN:")
    print(pgn_string.getvalue())