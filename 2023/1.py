import re
import sys

digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit_regexp = "(?=(\d|one|two|three|four|five|six|seven|eight|nine))"

lines = sys.stdin.readlines()

total = 0

for l in lines:
    numbers = []
    ms = re.finditer(digit_regexp, l)

    for m in ms:
        g = m.group(1)
        if g in digits:
            n = digits.index(g) + 1
        else:
            n = int(g)
        numbers.append(n)

    total += numbers[0] * 10 + numbers[-1]

print(total)
