#!/usr/bin/python3

# AOC 2023 Day 7 solution, part I: #########
# Completed 2744 iterations in 1m 0s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     37.50μs    36.92μs   2.94μs
# Execute  21.83ms    21.80ms   165.64μs
# Total    21.87ms    21.84ms   166.08μs

# AOC 2023 Day 7 solution, part II: #########
# Completed 185 iterations in 1m 0s.
#          Average    Median    Std. Dev.
# -------  ---------  --------  -----------
# Read     50.53μs    41.92μs   16.64μs
# Execute  324.35ms   322.81ms  4.67ms
# Total    324.40ms   322.85ms  4.68ms

import typing
from typing import Generator
from re import finditer
from re import compile as regex_compile
from enum import Enum
from functools import cmp_to_key
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(7)

variable_FLAGS = {'fix': False}

HAND_AND_BID_PATTERN = regex_compile('([AKQJT98765432]{5})\s+(\d+)')

CARD_VALUE_TABLE = {'A': 14, 'K': 13, 'Q': 12,
                    'J': 11, 'T': 10, '9': 9,
                    '8': 8,  '7': 7,  '6': 6,
                    '5': 5,  '4': 4,  '3': 3, '2': 2}

CARD_VALUE_TABLE_P2 = {'A': 14, 'K': 13, 'Q': 12,
                                'T': 10, '9': 9,
                       '8': 8,  '7': 7,  '6': 6,
                       '5': 5,  '4': 4,  '3': 3, '2': 2,
                       'J': 1}

NON_JOKER_CARDS = ('A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2')

class HandType(Enum):
	HIGH_CARD = 0
	ONE_PAIR = 1
	TWO_PAIR = 2
	THREE_OF_A_KIND = 3
	FULL_HOUSE = 4
	FOUR_OF_A_KIND = 5
	FIVE_OF_A_KIND = 6

	def __lt__(self, other):
		if self.__class__ == other.__class__:
			return self.value < other.value
		return NotImplemented

def get_hand_type_p1(hand: str) -> HandType:
	'''Returns the type of a hand assuming J=Jack'''
	number_of_distinct_cards = len(set(hand))
	# If there is only one kind of card, it's a "Five of a kind".
	if number_of_distinct_cards == 1:
		return HandType.FIVE_OF_A_KIND
	# If there are two types of cards it's either "Full House" or "Four of a kind".
	if number_of_distinct_cards == 2:
		# Boolean logic magic. If you wanna know how this works, figure it out on paper.
		# Can't help you there, sorry.
		hand = sorted(list(hand))
		if (hand[0] == hand[1]) and (hand[3] == hand[4]):
			return HandType.FULL_HOUSE
		else:
			return HandType.FOUR_OF_A_KIND
	# If there are three types of cards it's either "Three of a kind" or "Two pair".	
	if number_of_distinct_cards == 3:
		# More logic magic.
		hand = sorted(list(hand))
		if (hand[2] == hand[3]) ^ ((hand[3] != hand[4]) & (hand[0] == hand[1])):
			return HandType.THREE_OF_A_KIND
		else:
			return HandType.TWO_PAIR
	# If there are 4 different types of cards, it's a "One pair".
	# Because there is one pair.
	if number_of_distinct_cards == 4:
		return HandType.ONE_PAIR
	# If there are 5 different types of cards, it's a "High card" (why?).
	if number_of_distinct_cards == 5:
		return HandType.HIGH_CARD

def generate_possible_hands(hand: str) -> Generator[tuple, None, None]:
	'''Recursively generate all possible hands one could get
	by replacing all Joker cards with non-joker cards.'''
	no_jokers = True
	for i, card in enumerate(hand):
			if card == 'J':
				no_jokers = False
				for replacement in NON_JOKER_CARDS:
					new_hand = hand[:i] + replacement + hand[i+1:]
					yield from generate_possible_hands(new_hand)
	if no_jokers:
		yield hand

# This is bruteforce, but doing this in non-bruteforce way would
# require to change the way hands are stored and handled.
def get_hand_type(hand: str) -> HandType:
	'''Returns the type of a hand assuming J=Jack'''
	# If solving Part II.
	if variable_FLAGS['fix']:
		# If all cards are Jokers, it's a "Five of a kind".
		if hand == 'JJJJJ':
			return HandType.FIVE_OF_A_KIND
		# If four of the cards are Jokers, hand can always be made into a "Five of a kind".
		if hand.count('J') == 4:
			return HandType.FIVE_OF_A_KIND
		# Check every possible way to replace Jokers by different cards, take best result.
		return max( (get_hand_type_p1(hand_) for hand_ in generate_possible_hands(hand)) )
	# If solving Part I ... use that function instead.
	else:
		return get_hand_type_p1(hand)

def compare_two_hands(hand_1: dict, hand_2: dict) -> int:
	# Choose how strong J is depending on whether we are solving P I or P II.
	card_value_table = CARD_VALUE_TABLE_P2 if variable_FLAGS['fix'] else CARD_VALUE_TABLE

	# If one of the hands has a better type it wins.
	if hand_1['type'] < hand_2['type']:
		return -1
	if hand_1['type'] > hand_2['type']:
		return 1

	# The first place hands differ in, whichever hand's card is higher, wins.
	for i in range(5):
		if card_value_table[hand_1['hand'][i]] < card_value_table[hand_2['hand'][i]]:
			return -1
		if card_value_table[hand_1['hand'][i]] > card_value_table[hand_2['hand'][i]]:
			return 1

	return 0 # Wow! Those hands are the exact same!


def solve(input_: str, flags: dict) -> int:
	# Put flags into a GLOBAL VARIABLE to be used by other functions.
	global variable_FLAGS
	variable_FLAGS = flags

	total_winnings = 0
	ranked_hands_list = []

	# Find hands and bids in input, figure out the "type" of each hand.
	for hand_and_bid_match in HAND_AND_BID_PATTERN.finditer(input_):
		hand = hand_and_bid_match.group(1)
		bid = int(hand_and_bid_match.group(2))
		type_ = get_hand_type(hand)
		ranked_hands_list.append({
			'hand': hand,
			'bid': bid,
			'type': type_
		})

	# Produce a ranking of all cards.
	ranked_hands_list.sort(key=cmp_to_key(compare_two_hands))

	# Calculate total winnings
	for rank, hand in enumerate(ranked_hands_list, 1):
		total_winnings += rank * hand['bid']
	return total_winnings


if __name__ == '__main__':
	solve = arparse_and_time_wrapper(solve)
	solve()
