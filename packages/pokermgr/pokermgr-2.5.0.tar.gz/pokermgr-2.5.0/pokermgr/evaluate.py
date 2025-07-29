"""Poker Hand Evaluation Module

This module provides functionality to evaluate poker hands and determine the winner(s)
among multiple players. It handles the core logic for comparing hand strengths
based on standard poker hand rankings.

Functions:
    get_winners: Determines the winning player(s) based on their best 5-card hand
                evaluated against the community cards.
"""
from itertools import combinations
from typing import List, Tuple
from cardspy.card import extract_cards, cards_mask
from pokermgr.player import TablePlayer, BoardPlayer
from pokermgr.funcs import get_hand_type_weight
from pokermgr.hand import Hand


def get_winners(
    board_cards_key: int,
    players: List[TablePlayer]
) -> List[BoardPlayer]:
    """
    Determine the winning player(s) based on their best 5-card hand evaluated against
    the community cards.

    Args:
        board_cards_key: Integer bitmask representing the community cards.
        players: List of TablePlayer instances representing the players in the hand.

    Returns:
        A list of BoardPlayer instances representing the winning players.
    """
    if board_cards_key == 0:
        return []
    table_players = [
        player.to_board_player()
        for player in players
    ]

    # Calculate best hand for each player
    for player in table_players:
        best_hand = _get_player_best_hand(player, board_cards_key)
        player.hand = best_hand
        print(f"BEST HAND: {player.code}: {player.hand.weight}")

    # Find winners based on best weights
    return _determine_winners_from_hands(table_players)


def _get_player_best_weight(player: TablePlayer, board_cards_key: int) -> int:
    """Calculate the best possible hand weight for a player."""
    player_cards_count = player.hole_cards.key.bit_count()

    if player_cards_count == 2:
        return _get_holdem_best_weight(player, board_cards_key)
    elif player_cards_count >= 4:
        return _get_omaha_best_weight(player, board_cards_key)

    return 0


def _get_player_best_hand(player: BoardPlayer, board_cards_key: int) -> Hand:
    """Calculate the best possible hand weight for a player."""
    player_cards_count = player.hole_cards.key.bit_count()

    if player_cards_count < 2:
        raise ValueError("Player must have at least 2 hole cards")
    if player_cards_count == 2:
        return _get_holdem_best_hand(player, board_cards_key)
    if player_cards_count >= 4:
        return _get_omaha_best_hand(player, board_cards_key)

    return Hand(0)


def _get_holdem_best_weight(player: TablePlayer, board_cards_key: int) -> int:
    """Calculate best weight for Hold'em game (2 hole cards)."""
    all_cards_key = player.hole_cards.key | board_cards_key
    all_cards = extract_cards(all_cards_key)

    best_weight = 0
    for combo in combinations(all_cards, 5):
        combo_key = cards_mask(list(combo))
        weight, _, _ = get_hand_type_weight(combo_key)
        best_weight = max(best_weight, weight)

    return best_weight


def _get_holdem_best_hand(player: BoardPlayer, board_cards_key: int) -> Hand:
    """Calculate best weight for Hold'em game (2 hole cards)."""
    all_cards_key = player.hole_cards.key | board_cards_key
    all_cards = extract_cards(all_cards_key)

    best_hand = Hand(0)
    for combo in combinations(all_cards, 5):
        combo_key = cards_mask(list(combo))
        weight, type_key, type_name = get_hand_type_weight(combo_key)
        if weight > best_hand.weight:
            best_hand = Hand(combo_key)
            best_hand.type_key = type_key
            best_hand.type_name = type_name
            best_hand.weight = weight

    return best_hand


def _get_omaha_best_weight(player: TablePlayer, board_cards_key: int) -> int:
    """Calculate best weight for Omaha game (4+ hole cards)."""
    player_cards = extract_cards(player.hole_cards.key)
    board_cards = extract_cards(board_cards_key)

    best_weight = 0
    for player_cards_combo in combinations(player_cards, 2):
        for board_cards_combo in combinations(board_cards, 3):
            combo = player_cards_combo + board_cards_combo
            combo_key = cards_mask(list(combo))
            weight, _, _ = get_hand_type_weight(combo_key)
            best_weight = max(best_weight, weight)

    return best_weight


def _get_omaha_best_hand(player: BoardPlayer, board_cards_key: int) -> Hand:
    """Calculate best weight for Omaha game (4+ hole cards)."""
    player_cards = extract_cards(player.hole_cards.key)
    board_cards = extract_cards(board_cards_key)

    best_hand = Hand(0)
    for player_cards_combo in combinations(player_cards, 2):
        for board_cards_combo in combinations(board_cards, 3):
            combo = player_cards_combo + board_cards_combo
            combo_key = cards_mask(list(combo))
            weight, type_key, type_name = get_hand_type_weight(combo_key)
            if weight > best_hand.weight:
                best_hand = Hand(combo_key)
                best_hand.type_key = type_key
                best_hand.type_name = type_name
                best_hand.weight = weight

    return best_hand


def _determine_winners_from_weights(
    player_weights: List[Tuple[TablePlayer, int]]
) -> List[TablePlayer]:
    """Determine winners from list of (player, weight) tuples."""
    if not player_weights:
        return []

    # Find the maximum weight
    max_weight = max(weight for _, weight in player_weights)

    # Return all players with the maximum weight
    return [player for player, weight in player_weights if weight == max_weight]


def _determine_winners_from_hands(
    players: List[BoardPlayer]
) -> List[BoardPlayer]:
    """Determine winners from list of (player, weight) tuples."""
    if not players:
        return []

    winners: List[BoardPlayer] = []

    # Find the maximum weight
    best_weight = 0
    for player in players:
        if player.hand.weight > best_weight:
            best_weight = player.hand.weight
            winners = [player]
        elif player.hand.weight == best_weight:
            winners.append(player)

    return winners
