from dataclasses import dataclass
from docutils.nodes import description
from parameters import *
import random

@dataclass
class Status: # General Status
    history_decisions_opponent: list[int]
    history_decisions_own: list[int]
    total_steps: int


class TitForTat():
    def __call__(self, status: Status):
        if status.history_decisions_opponent == []:
            return 0
        else:
            # just copy the last decision of opponent
            return status.history_decisions_opponent[-1]


class TidemanAndChieruzzi():
    def __init__(self):
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0
        self.score_self = 0
        self.score_oppo = 0
        self.last_fresh_start = 0
        self.fresh_start_flag = False
        self.opponent_defections = 0

    def __call__(self, status: Status):
        if not status.history_decisions_opponent:
            return 0

        step = len(status.history_decisions_own)

        # calculate the score of last time
        a, b = status.history_decisions_own[-1], status.history_decisions_opponent[-1]
        self.score_self += reward[a][b][0]
        self.score_oppo += reward[a][b][1]

        # update betrayal count
        if b == 1:
            self.opponent_defections += 1

        # fresh start the second cooperation
        if self.fresh_start_flag:
            self.fresh_start_flag = False
            return 0

        # whether it accomplished the fresh start
        rounds_since_fresh = step - self.last_fresh_start
        rounds_left = status.total_steps - step
        valid_fresh = (rounds_since_fresh >= 20 or self.last_fresh_start == 0) and \
                      (self.score_self - self.score_oppo >= 10) and \
                      (rounds_left >= 10) and \
                      (b == 0)

        if valid_fresh:
            N = len(status.history_decisions_opponent)
            std_dev = (N ** 0.5) / 2
            lower = N / 2 - 3 * std_dev
            upper = N / 2 + 3 * std_dev
            if self.opponent_defections <= lower or self.opponent_defections >= upper:
                self.last_fresh_start = step
                self.retaliation_length = 0
                self.retaliation_remaining = 0
                self.is_retaliating = False
                self.opponent_defections = 0
                self.fresh_start_flag = True
                return 0  # fresh start first round of cooperation

        # punish
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False
            return 1

        if b == 1:
            self.is_retaliating = True
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length - 1
            return 1

        # cooperate at first
        return 0


class Random():
    def __call__(self, status: Status):
        return random.randint(0, len(id_to_decision) - 1)


class Grofman():
    def __call__(self, status: Status):
        if not status.history_decisions_opponent:
            return 0
        elif status.history_decisions_opponent[-1] == status.history_decisions_own[-1]:
            return 0
        else:
            return 0 if random.random() < 2 / 7 else 1 # 2/7 probability returns 0



if __name__ == '__main__':
    status = Status([1, 1, 0, 1, 0], [0, 0, 1, 1, 0], 10)
    test_method = TidemanAndChieruzzi()
    print(test_method(status))
