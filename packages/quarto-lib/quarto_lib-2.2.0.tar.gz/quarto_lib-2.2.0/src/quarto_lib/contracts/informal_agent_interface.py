from typing import Optional, Tuple

from quarto_lib.contracts.game_state import GameState
from quarto_lib.types.cell import Cell
from quarto_lib.types.piece import Piece


class InformalAgentInterface:
    def choose_initial_piece(self) -> Piece:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def complete_turn(self, game: GameState) -> Tuple[Cell, Optional[Piece]]:
        raise NotImplementedError("This method should be implemented by subclasses.")
