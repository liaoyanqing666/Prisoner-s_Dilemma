from approches import *
import pandas as pd
import numpy as np

def multiplayer(players, rounds, times=1):
    player_names = [cls.__name__ for cls in players]
    num_players = len(players)

    scores_matrix = pd.DataFrame(0.0, index=player_names, columns=player_names)

    for _ in range(times):
        for i in range(num_players):
            for j in range(i, num_players):
                player1 = players[i]()
                player2 = players[j]()

                history1 = []
                history2 = []

                score1 = 0
                score2 = 0

                for step in range(rounds):
                    status1 = Status(history_decisions_opponent=history2,
                                     history_decisions_own=history1,
                                     total_steps=step)
                    status2 = Status(history_decisions_opponent=history1,
                                     history_decisions_own=history2,
                                     total_steps=step)

                    decision1 = player1(status1)
                    decision2 = player2(status2)

                    history1.append(decision1)
                    history2.append(decision2)

                    r1, r2 = reward[decision1][decision2]
                    score1 += r1
                    score2 += r2

                scores_matrix.iloc[i, j] += score1
                if i != j: # if self-play, don't double count
                    scores_matrix.iloc[j, i] += score2

    scores_matrix /= times
    return scores_matrix


def append_average_and_sort(df):
    df_with_avg = df.copy()
    df_with_avg["Average"] = df_with_avg.mean(axis=1)
    df_with_avg = df_with_avg.sort_values(by="Average", ascending=False)
    return df_with_avg


if __name__ == "__main__":
    players = [
        TitForTat,
        TidemanAndChieruzzi,
        Grofman,
        Random,
    ]

    rounds = 200 # number of consecutive decision-making rounds conducted in a single experiment
    times = 100 # number of experiment

    result = multiplayer(players, rounds, times)
    print("Original result")
    print(result)

    print("Sorted result")
    result_with_avg = append_average_and_sort(result)
    print(result_with_avg)





