"""Poker Game Play

This module implements the core poker game logic, including game state management,
card dealing, and street progression. It supports multiple poker variants through
class inheritance and provides a flexible framework for different poker games.

Classes:
    GameStreet: Enum representing the different streets in a poker hand
    Game: Base class for poker games with common functionality
    GameTexasHoldem: Texas Hold'em specific game implementation
    GameTexasHoldemRegular: Regular Texas Hold'em with small/big blinds
    GameTexasHoldemBomb: Texas Hold'em variant with a bomb pot (forced all-in)
"""
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from cardspy.card import extract_cards
from cardspy.deck import Deck
from pokermgr.table import Table
from pokermgr.pot import Pot
from pokermgr.board import Board
from pokermgr.player import TablePlayer, PlayerStatus
from pokermgr.evaluate import get_winners


class GameStreet(Enum):
    """Represents the different streets in a poker hand.

    Streets progress from pre-flop to river, with each street representing
    a different stage of the hand where community cards are revealed and
    betting occurs.

    Attributes:
        PRE_FLOP: Initial street where players receive hole cards
        FLOP: Second street where the first three community cards are dealt
        TURN: Third street where the fourth community card is dealt
        RIVER: Final street where the fifth community card is dealt
    """
    PRE_FLOP = 1  # Initial street with hole cards only
    FLOP = 2     # First three community cards
    TURN = 3     # Fourth community card
    RIVER = 4    # Fifth and final community card


class Game(ABC):
    """Base class for poker games providing common functionality.

    This class handles the core game flow, including dealing cards, managing
    the board, and tracking game state. It serves as the foundation for
    different poker variants through inheritance.

    Args:
        key: Unique identifier for the game
        table: Table object containing player information
        initial_board_count: Number of boards to use (default: 1)

    Attributes:
        key: Unique game identifier
        table: Reference to the game table
        initial_board_count: Number of boards in play
        board_count: Current number of active boards
        boards: List of Board objects
        game_street: Current street of the game (from GameStreet enum)
        pots: List of active pots
        deck: Deck of cards
        player_to_act: Reference to the player whose turn it is to act
    """
    def __init__(
        self,
        key: int,
        table: Table,
        initial_board_count: int = 1
    ) -> None:
        self.key = key
        self.table = table
        self.initial_board_count = initial_board_count
        self.board_count = 0
        self.boards: list[Board] = []
        self.game_street = GameStreet.PRE_FLOP
        self.pots: list[Pot] = []
        self.deck = Deck()
        self.player_to_act = self.table.players[0]
        self.initiate_board()

    def initiate_board(self) -> None:
        """Initialize the specified number of boards for the game.

        This method creates the initial set of boards based on the
        initial_board_count. Each board will be assigned a unique ID.
        """
        while len(self.boards) < self.initial_board_count:
            self.add_board()

    def add_board(self) -> None:
        """Add a new board to the game.

        If boards already exist, the new board will be a copy of the most recent board.
        This ensures all boards are in sync when a new one is added mid-hand.
        Also updates all pots to track the new board.
        """
        # Create new board with incremented ID
        board_id = self.board_count + 1
        board = Board(board_id)

        # If boards exist, copy cards from the most recent board
        if self.board_count > 0:
            existing_board = self.boards[-1]
            board.add_cards(existing_board.cards)

        self.boards.append(board)
        self.board_count += 1

    def add_pot(self, stack: int = 0, players: Optional[List[TablePlayer]] = None) -> Pot:
        """Add a new pot to the game (e.g., side pots when players go all-in).

        Args:
            stack: Initial amount of chips for the new pot.
            players: Iterable of players eligible for the pot. Defaults to all current players.
        Returns:
            The newly created Pot object.
        """
        if players is None:
            players = list(self.table.players)
        key = len(self.pots) + 1
        new_pot = Pot(key, stack, players)
        self.pots.append(new_pot)
        return new_pot

    def deal_hole_cards(self, cards: Optional[List[int]] = None) -> None:
        """Deal hole cards to all players.

        Args:
            cards: Optional list of pre-determined cards to deal. If not provided,
                  cards will be dealt randomly from the deck.

        Raises:
            ValueError: If called on any street other than pre-flop or if the number
                     of provided cards doesn't match the number of players.
        """
        if self.game_street != GameStreet.PRE_FLOP:
            raise ValueError("Hole cards can only be dealt on the pre-flop")

        if cards:
            # Deal specified cards if provided (for testing/deterministic dealing)
            if len(cards) != len(self.table.players):
                raise ValueError("Number of cards must match number of players")
            for player in self.table.players:
                player.set_hole_cards(cards.pop(0))
        else:
            # Use the game-specific dealing logic
            self._core_deal_hole_cards()

    @abstractmethod
    def _core_deal_hole_cards(self) -> None:
        """Abstract method to handle game-specific hole card dealing logic.

        This method must be implemented by subclasses to define how hole cards
        are dealt for specific poker variants (e.g., 2 cards for Texas Hold'em,
        4 cards for Omaha, etc.).
        """

    def deal_flop(self, cards: Optional[List[int]] = None) -> None:
        """Deal the flop (first three community cards).

        Args:
            cards: Optional list of pre-determined cards to deal as the flop.
                  If provided, must contain one card per board.

        Raises:
            ValueError: If called on any street other than pre-flop or if the
                     number of provided cards doesn't match the number of boards.
        """
        if self.game_street != GameStreet.PRE_FLOP:
            raise ValueError("Flop can only be dealt on the pre-flop")

        if cards:
            # Deal specified cards if provided (for testing/deterministic dealing)
            if len(cards) != self.board_count:
                raise ValueError("Number of cards must match number of boards")
            for board in self.boards:
                board.add_cards(cards.pop(0))
        else:
            # Deal random cards from the deck
            for board in self.boards:
                board.add_cards(self.deck.deal_cards(3))

        # Advance game state to FLOP
        self.game_street = GameStreet.FLOP

    def deal_turn(self, cards: Optional[List[int]] = None) -> None:
        """Deal the turn (fourth community card).

        Args:
            cards: Optional list of pre-determined cards to deal as the turn.
                  If provided, must contain one card per board.

        Raises:
            ValueError: If called on any street other than flop or if the
                     number of provided cards doesn't match the number of boards.
        """
        if self.game_street != GameStreet.FLOP:
            raise ValueError("Turn can only be dealt on the flop")
        if cards:
            if len(cards) != self.board_count:
                raise ValueError("Number of cards must match number of boards")
            for board in self.boards:
                board.add_cards(cards.pop(0))
        else:
            for board in self.boards:
                board.add_cards(self.deck.deal_cards(1))
        self.game_street = GameStreet.TURN

    def deal_river(self, cards: Optional[List[int]] = None) -> None:
        """Deal the river (fifth community card).

        Args:
            cards: Optional list of pre-determined cards to deal as the river.
                  If provided, must contain one card per board.

        Raises:
            ValueError: If called on any street other than turn or if the
                     number of provided cards doesn't match the number of boards.
        """
        if self.game_street != GameStreet.TURN:
            raise ValueError("River can only be dealt on the turn")
        if cards:
            if len(cards) != self.board_count:
                raise ValueError("Number of cards must match number of boards")
            for board in self.boards:
                board.add_cards(cards.pop(0))
        else:
            for board in self.boards:
                board.add_cards(self.deck.deal_cards(1))
        self.game_street = GameStreet.RIVER

    def get_result(self) -> List[Dict[str, Any]]:
        """Return a list of dictionaries containing the result of the game.

        Each dictionary contains the key of a pot, the key of a board, and a list
        of the winners for that board. The winners are represented as a list of
        player keys.

        Returns:
            A list of dictionaries with the game result.
        """
        result: List[Dict[str, Any]] = []
        for pot in self.pots:
            boards_count = len(self.boards)
            players: List[TablePlayer] = [
                player for player in pot.players
                if player.status in [
                    PlayerStatus.INGAME,
                    PlayerStatus.ALLIN
                ]
            ]
            for board in self.boards:
                winning_players = get_winners(
                    board.cards,
                    players
                )
                winners = [
                    f"{player.code} - {extract_cards(player.hand.cards)} - {player.hand.type_name}"
                    for player in winning_players
                ]
                number_of_winners = len(winners)
                share_per_player = 0.0
                if pot.stack > 0 and number_of_winners > 0:
                    share_per_player = (pot.stack / boards_count) / number_of_winners
                result.append(
                    {
                        "pot": pot.key,
                        "board": board.key,
                        "share_per_player": share_per_player,
                        "winners": winners
                    }
                )
        return result


class GameTexasHoldem(Game):
    """Base class for Texas Hold'em poker games.

    This class implements Texas Hold'em specific rules, including dealing
    two hole cards to each player. It serves as a base class for different
    Texas Hold'em variants (e.g., regular, bomb pots).

    Args:
        key: Unique identifier for the game
        table: Table object containing player information
        initial_board_count: Number of boards to use (default: 1)
    """
    def __init__(
        self,
        key: int,
        table: Table,
        initial_board_count: int = 1
    ) -> None:
        self.initial_board_count = initial_board_count
        super().__init__(key, table, initial_board_count)

    def _core_deal_hole_cards(self) -> None:
        """Deal two hole cards to each player from the deck.

        This implements the standard Texas Hold'em dealing where each player
        receives exactly two private cards.
        """
        for player in self.table.players:
            player.set_hole_cards(self.deck.deal_cards(2))


class GameTexasHoldemRegular(GameTexasHoldem):
    """Standard Texas Hold'em game with small and big blinds.

    This class implements a regular Texas Hold'em game where players post
    small and big blinds, and betting proceeds in standard fashion.

    Args:
        key: Unique identifier for the game
        table: Table object containing player information
        small_blind: Size of the small blind
        big_blind: Size of the big blind
        initial_board_count: Number of boards to use (default: 1)

    Attributes:
        small_blind: Size of the small blind
        big_blind: Size of the big blind
    """
    def __init__(
        self,
        key: int,
        table: Table,
        small_blind: int,
        big_blind: int,
        initial_board_count: int = 1
    ) -> None:
        super().__init__(key, table, initial_board_count)
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.initiate_board()


class GameTexasHoldemBomb(GameTexasHoldem):
    """Texas Hold'em Bomb Pot variant where all players are all-in pre-flop.

    In this variant, all players must post a blind and are automatically all-in
    before any cards are dealt. The hand then proceeds with community cards being
    dealt normally, but with no further betting rounds.

    Args:
        key: Unique identifier for the game
        table: Table object containing player information
        blind: Mandatory blind amount that all players must post
        initial_board_count: Number of boards to use (default: 1)

    Attributes:
        blind: Fixed blind amount for the bomb pot
    """
    def __init__(
        self,
        key: int,
        table: Table,
        blind: int,
        initial_board_count: int = 1
    ) -> None:
        super().__init__(key, table, initial_board_count)
        self.blind = blind
        # Initialize the pot with blinds from all players
        # self.pots[0].stack = self.blind * len(self.table.players)
        self.add_pot(self.blind * len(self.table.players))
