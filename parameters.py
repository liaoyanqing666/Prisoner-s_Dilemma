id_to_decision = {0: "Cooperation", 1: "Betrayal"}
reward = [[(3, 3), (0, 5)],
          [(5, 0), (1, 1)]]
# this reward corresponding to decision
# [(0, 0), (0, 1)]
# [(1, 0), (1, 1)]

assert len(reward) == len(id_to_decision) and all(len(row) == len(id_to_decision) for row in reward) # assert reward can cover all situations
