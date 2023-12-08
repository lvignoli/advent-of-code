import sys
from enum import Enum
from collections import defaultdict

lines = sys.stdin.readlines()


class Type(Enum):
    FiveOfAKind = 0
    FourOfAKind = 1
    Full = 2
    Three = 3
    TwoPairs = 4
    OnePair = 5
    HighCard = 6


def convert_to_value(x) -> int:
    try:
        y = int(x)
    except:
        match x:
            case "T":
                y = 10
            case "J":
                y = 11
            case "Q":
                y = 12
            case "K":
                y = 13
            case "A":
                y = 14
            case _:
                raise Exception

    return y


hands = []

for l in lines:
    counts = defaultdict(int)
    left, right = l.split()
    for c in left:
        counts[c] += 1

    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    if counts[0][1] == 5:
        rank = Type.FiveOfAKind
    elif counts[0][1] == 4:
        rank = Type.FourOfAKind
    elif counts[0][1] == 3:
        if counts[1][1] == 2:
            rank = Type.Full
        else:
            rank = Type.Three
    elif counts[0][1] == 2:
        if counts[1][1] == 2:
            rank = Type.TwoPairs
        else:
            rank = Type.OnePair
    else:
        rank = Type.HighCard

    bid = int(right)

    hand = (rank, [convert_to_value(c) for c in left], bid)
    hands.append(hand)


hands = sorted(hands, key=lambda x: (-x[0].value, x[1]))
tot = 0
for i, h in enumerate(hands):
    tot += h[2] * (i + 1)
print(tot)

# 2


def convert_to_value_part_2(x) -> int:
    try:
        y = int(x)
    except:
        match x:
            case "J":
                y = 1
            case "T":
                y = 10
            case "Q":
                y = 12
            case "K":
                y = 13
            case "A":
                y = 14
            case _:
                raise Exception

    return y


hands = []
lefts = []

for l in lines:
    counts = defaultdict(int)
    left, right = l.split()
    lefts.append(left)
    for c in left:
        counts[c] += 1

    joker = counts["J"]
    del counts["J"]

    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    if len(counts) <= 1:
        # Only jokers or a single figure and jokers
        top_count = 5
        second_count = 0
    else:
        top_count = counts[0][1] + joker
        second_count = counts[1][1]

    if top_count == 5:
        rank = Type.FiveOfAKind
    elif top_count == 4:
        rank = Type.FourOfAKind
    elif top_count == 3:
        if second_count == 2:
            rank = Type.Full
        else:
            rank = Type.Three
    elif top_count == 2:
        if second_count == 2:
            rank = Type.TwoPairs
        else:
            rank = Type.OnePair
    else:
        rank = Type.HighCard

    bid = int(right)

    hand = (rank, [convert_to_value_part_2(c) for c in left], bid)
    hands.append(hand)

    print(left, hand)


foo = zip(lefts, hands)
foo = sorted(foo, key=lambda x: (-x[1][0].value, x[1][1]))

hands = sorted(hands, key=lambda x: (-x[0].value, x[1]))


print()
print("SORTED")
print()
for l, h in foo:
    print(l, h)

tot = 0
for i, h in enumerate(hands):
    tot += h[2] * (i + 1)
print(tot)
