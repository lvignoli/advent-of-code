from __future__ import annotations

import math
import sys
from collections import deque
from typing import Any, Callable, Iterable

queue = deque()
counts = {False: 0, True: 0}
done = False


def parse(input: str) -> dict[str, Module]:
    modules: dict[str, Module] = {}

    for l in input.splitlines():
        left, right = l.split("->")
        left = left.strip()

        if left[0] == "%":
            name = left[1:]
            modules[name] = FlipFlop(name)
        elif left[0] == "&":
            name = left[1:]
            modules[name] = Conjunction(name)
        elif left == "broadcaster":
            modules[left] = Broadcaster(left)

    for l in input.splitlines():
        left, right = l.split("->")
        left = left.strip()
        name = left[1:] if left[0] in ("%", "&") else left

        sends_to = right.split(",")
        for s in sends_to:
            s = s.strip()
            if s not in modules:
                modules[s] = Output(s)
            modules[name].add_subscriber(modules[s])
            m = modules[s]
            if isinstance(m, Conjunction):
                m.declare_input(name)

    return modules


targets = ["pv", "qh", "xm", "hz"]
button_count = 0


def count_me_as_cycle(name: str):
    cycles[name] = button_count


class Module:
    def __init__(self, name: str) -> None:
        self.name = name
        self.state = False
        self.subscribers = {}

    def add_subscriber(self, m: Module):
        self.subscribers[m.name] = m.update

    def update(self, from_name: str, signal: bool):
        raise NotImplementedError

    def send(self):
        if self.name in targets and self.state:
            count_me_as_cycle(self.name)
        for name in self.subscribers:
            # if name == "rx":
            # print("send to rx: ", self.state)
            # global done
            # done = True

            # print(f"{self.name}({self.state}) -{self.state}-> {name}")
            update_func = self.subscribers[name]
            counts[self.state] += 1
            update_func(self.name, self.state)


class FlipFlop(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def update(self, from_name: str, signal: bool):
        if not signal:
            self.state = not self.state
            queue.append(self.name)


class Conjunction(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.last_pulses: dict[str, bool] = {}

    def add_subscriber(self, m: Module):
        # self.last_pulses[m.name] = False
        return super().add_subscriber(m)

    def declare_input(self, name: str):
        self.last_pulses[name] = False
        # print(f"declared {name}")

    def create_update_func(self, connected_to: str, signal: bool):
        self.last_pulses[connected_to] = False

        def update(signal: bool):
            self.last_pulses[connected_to] = signal
            self.state = not all(self.last_pulses.values())

        return update

    def update(self, from_name: str, signal: bool):
        self.last_pulses[from_name] = signal
        self.state = not all(self.last_pulses.values())
        queue.append(self.name)


class Broadcaster(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def update(self, from_name: str, signal: bool):
        queue.append(self.name)


class Button(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class Output(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def update(self, from_name: str, signal: bool):
        pass


modules = parse(sys.stdin.read())
modules["button"] = Button("button")
modules["button"].add_subscriber(modules["broadcaster"])

# PART 1
# counts = {False: 0, True: 0}
# for _ in range(1000):
#     queue.append("button")
#     while len(queue) > 0:
#         name = queue.popleft()
#         modules[name].send()
# print(counts)
# print(counts[False] * counts[True])

# 2

# # Find the antecedent of rx
# antecendent_name = ""
# for name, m in modules.items():
#     if "rx" in m.subscribers:
#         antecedent_name = name
#         break

# # Find the antecedent of the antecedent
# targets = []
# for name, m in modules.items():
#     if antecedent_name in m.subscribers:
#         targets.append(name)

cycles = {name: 0 for name in targets}
print(targets)


while not done:
    button_count += 1
    queue.append("button")
    while len(queue) > 0:
        name = queue.popleft()
        modules[name].send()

    for name in targets:
        print(modules[name].state)
        if modules[name].state:
            cycles[name] = button_count
            print(cycles)
    for n in cycles:
        if cycles[n] > 0 and n in targets:
            targets.remove(n)

    if len(targets) == 0:
        done = True

print(cycles)
print(math.lcm(*cycles.values()))
