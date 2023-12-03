import sys

lines = sys.stdin.readlines()

ret = 0
gameid = 0

# 1
# for l in lines:
#     gameid += 1

#     counts = {}
#     counts["blue"] = 0
#     counts["red"] = 0
#     counts["green"] = 0
#     _, a = l.split(":")
#     sets = a.split(";")

#     to_count = True

#     for s in sets:
#         dices = s.split(",")
#         for d in dices:
#             n, c = d.strip().split(" ")
#             # print(n, c)
#             counts[c] = int(n)

#         possible = (
#             (counts["red"] <= 12) and (counts["green"] <= 13) and (counts["blue"] <= 14)
#         )
#         print(possible)
#         if not possible:
#             to_count = False

#     if to_count:
#         ret += gameid

# print(ret)


for l in lines:
    gameid += 1

    counts = {}
    counts["blue"] = [0]
    counts["red"] = [0]
    counts["green"] = [0]
    _, a = l.split(":")
    sets = a.split(";")

    to_count = True

    for s in sets:
        dices = s.split(",")
        for d in dices:
            n, c = d.strip().split(" ")
            # print(n, c)
            counts[c].append(int(n))

    fewest_red = max(counts["red"])
    fewest_green = max(counts["green"])
    fewest_blue = max(counts["blue"])

    power = fewest_red * fewest_green * fewest_blue
    print(power)
    ret += power
    #     possible = (
    #         (counts["red"] <= 12) and (counts["green"] <= 13) and (counts["blue"] <= 14)
    #     )
    #     print(possible)
    #     if not possible:
    #         to_count = False

    # if to_count:
    #     ret += gameid

print(ret)
