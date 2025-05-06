from dataclasses import dataclass
from parameters import *
import random
from scipy.stats import chisquare

@dataclass
class Status: # General Status
    history_decisions_opponent: list[int]
    history_decisions_own: list[int]
    total_steps: int


class TitForTat:
    def __call__(self, status: Status):
        if status.history_decisions_opponent == []:
            return 0
        else:
            # just copy the last decision of opponent
            return status.history_decisions_opponent[-1]


class TidemanAndChieruzzi:
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


class Nydegger:
    def __init__(self):
        self.As = {1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61}

    def __call__(self, status: Status):
        step = len(status.history_decisions_own)

        # Begin with tit for tat for the first three moves
        if step == 0:
            return 0
        if step == 1:
            return status.history_decisions_opponent[-1]
        if step == 2:
            if status.history_decisions_opponent[:2] == [1, 0] and status.history_decisions_own[:2] == [0, 1]:
                return 1
            return status.history_decisions_opponent[-1]

        def score(a, b):
            if a == 0 and b == 0:
                return 0
            if a == 0 and b == 1:
                return 2
            if a == 1 and b == 0:
                return 1
            return 3

        weights = [16, 4, 1]
        A = sum(w * score(status.history_decisions_own[-i], status.history_decisions_opponent[-i])
                for i, w in zip([1, 2, 3], weights))

        return 1 if A in self.As else 0


class Grofman:
    def __call__(self, status: Status):
        if not status.history_decisions_opponent:
            return 0
        elif status.history_decisions_opponent[-1] == status.history_decisions_own[-1]:
            return 0
        else:
            return 0 if random.random() < 2 / 7 else 1 # 2/7 probability returns 0


class Shubik:
    def __init__(self):
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0

    def __call__(self, status: Status):
        if not status.history_decisions_opponent:
            return 0

        # If it is in the period of retaliation, return betrayal
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False
            return 1

        # If the last decision of the opponent is betrayal, retaliate
        if status.history_decisions_own[-1] == 0 and status.history_decisions_opponent[-1] == 1:
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length - 1
            self.is_retaliating = True
            return 1

        return 0  # 默认合作


class SteinAndRapoport:
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.opponent_is_random = False

    def __call__(self, status: Status):
        step = len(status.history_decisions_own)

        if step < 4:
            return 0
        if status.total_steps - step <= 2:
            return 1

        if step % 15 == 0:
            coop = status.history_decisions_opponent.count(0)
            defe = status.history_decisions_opponent.count(1)
            if coop + defe > 0:
                p = chisquare([coop, defe]).pvalue
                self.opponent_is_random = p >= self.alpha

        if self.opponent_is_random:
            return 1
        return status.history_decisions_opponent[-1]


class Grudger:
    def __call__(self, status: Status):
        if 1 in status.history_decisions_opponent:
            return 1
        else:
            return 0


class Davis:
    def __init__(self, rounds_to_cooperate: int = 10):
        self.rounds_to_cooperate = rounds_to_cooperate

    def __call__(self, status: Status):
        if len(status.history_decisions_opponent) < self.rounds_to_cooperate:
            return 0

        if 1 in status.history_decisions_opponent:
            return 1
        else:
            return 0


class Graaskamp:
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.opponent_is_random = False
        self.next_random_defection_turn = None

    def __call__(self, status: Status):
        step = len(status.history_decisions_own)

        if not status.history_decisions_opponent:
            return 0

        if step < 56:
            if status.history_decisions_opponent[-1] == 1 or step == 50:
                return 1
            return 0

        coop = status.history_decisions_opponent.count(0)
        defe = status.history_decisions_opponent.count(1)
        if coop + defe > 0:
            p = chisquare([coop, defe]).pvalue
            if p >= self.alpha:
                self.opponent_is_random = True

        if self.opponent_is_random:
            return 1

        if all(
            i > 0 and status.history_decisions_opponent[i] == status.history_decisions_own[i - 1]
            for i in range(1, step)
        ) or status.history_decisions_opponent == status.history_decisions_own:
            return status.history_decisions_opponent[-1]

        if self.next_random_defection_turn is None:
            self.next_random_defection_turn = step + random.randint(5, 15)

        if step == self.next_random_defection_turn:
            self.next_random_defection_turn = step + random.randint(5, 15)
            return 1

        return 0


class Downing:
    def __init__(self):
        self.coop_after_c = 0
        self.coop_after_d = 0

    def __call__(self, status: Status):
        step = len(status.history_decisions_own)

        if step == 0:
            return 1  # round 1: defect
        if step == 1:
            if status.history_decisions_opponent[0] == 0:
                self.coop_after_c += 1
            return 1  # round 2: defect

        if status.history_decisions_own[-2] == 0 and status.history_decisions_opponent[-1] == 0:
            self.coop_after_c += 1
        if status.history_decisions_own[-2] == 1 and status.history_decisions_opponent[-1] == 0:
            self.coop_after_d += 1

        coop_count = status.history_decisions_own.count(0)
        defe_count = status.history_decisions_own.count(1)

        alpha = self.coop_after_c / (coop_count + 1)
        beta = self.coop_after_d / max(defe_count, 2)

        R, P, S, T = reward[0][0][0], reward[1][1][0], reward[0][1][0], reward[1][0][0]

        e_c = alpha * R + (1 - alpha) * S
        e_d = beta * T + (1 - beta) * P

        if e_c > e_d:
            return 0
        elif e_d > e_c:
            return 1
        else:
            return 1 - status.history_decisions_own[-1]


class Feld:
    def __init__(self, start_prob=1.0, end_prob=0.5, decay_rounds=200):
        self.start_prob = start_prob
        self.end_prob = end_prob
        self.decay_rounds = decay_rounds

    def __call__(self, status: Status):
        step = len(status.history_decisions_own)

        if step == 0:
            return 0

        if status.history_decisions_opponent[-1] == 1:
            return 1

        slope = (self.end_prob - self.start_prob) / self.decay_rounds
        prob = max(self.start_prob + slope * step, self.end_prob)

        return 0 if random.random() < prob else 1


class Joss:
    def __init__(self, p=0.9):
        self.p = p

    def __call__(self, status: Status):
        if not status.history_decisions_opponent:
            return 0

        if status.history_decisions_opponent[-1] == 1:
            return 1

        if random.random() < self.p:
            return 0
        else:
            return 1


class Tullock:
    def __call__(self, status: Status):
        if len(status.history_decisions_own) < 11:
            return 0

        coop_count = status.history_decisions_opponent[-10:].count(0)
        coop_p = max(float(coop_count) / 10 - 0.1, 0)

        return 0 if random.random() < coop_p else 1


class Collaborator:
    def __call__(self, status: Status):
        return 0


class Betrayer:
    def __call__(self, status: Status):
        return 1


class Random:
    def __call__(self, status: Status):
        return random.randint(0, len(id_to_decision) - 1)


class TwoTitsForTat:
    def __call__(self, status: Status):
        if len(status.history_decisions_own) == 0:
            return 0
        elif len(status.history_decisions_own) == 1:
            return status.history_decisions_opponent[-1]
        elif 1 in status.history_decisions_opponent[-2:]:
            return 1
        else:
            return 0


class TitForTwoTats:
    def __call__(self, status: Status):
        if len(status.history_decisions_own) < 2:
            return 0
        elif list(status.history_decisions_opponent[-2:]) == [1, 1]:
            return 1
        else:
            return 0


# Test a certain implementation
if __name__ == '__main__':
    status = Status([1, 1, 0, 1, 0], [0, 0, 1, 1, 0], 10)
    test_method = TidemanAndChieruzzi()
    print(test_method(status))
