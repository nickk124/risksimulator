import argparse
from argparse import RawTextHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

""" NOTATION
A == attackers
D == defenders


"""

def simulateWar(N_A, N_D): # here, a war is a sequence of battle between two territories. ASSUMING ATTACKER ATTACKS AS LONG AS THEY CAN
    while N_A > 1 and N_D > 0:
        n_lose_A, n_lose_D = simulateBattle(N_A, N_D)
        N_A -= n_lose_A
        N_D -= n_lose_D

    return int(N_A > 1) # 1=True if attacker wins, 0=False if defender wins


def simulateBattle(n_A, n_D): # a battle is just where both players roll
    n_dice_A = np.min(np.array([3, n_A - 1]))     # number of dice attacker rolls ASSUMING THEY ATTACK WITH AS MUCH AS POSSIBLE
    n_dice_D = np.min(np.array([2, n_D]))         # number of dice defender rolls ASSUMING THEY DEFEND WITH AS MUCH AS POSSIBLE
    # choosing the number you're attacking/defending with totally randomly is unrealistic, so I did the above 
    # but theres no a priori reason to assign probabilitiy to these choices; generally, the best choice is to attack/defend with the most,
    # so I defaulted to that.

    # roll the dice:
    dice_A_sorted = np.sort(np.random.randint(1, high=7, size=n_dice_A))[::-1] # sorted DESCENDING
    dice_D_sorted = np.sort(np.random.randint(1, high=7, size=n_dice_D))[::-1]

    n_lose_A, n_lose_D = 0, 0   # number of pieces lost

    n_compare = np.min(np.array([n_dice_A, n_dice_D]))    # number of dice pairs to compare
    for i in range(n_compare): 
        if dice_A_sorted[i] > dice_D_sorted[i]:
            n_lose_D += 1
        else:
            n_lose_A += 1

    return n_lose_A, n_lose_D

def simulateWars(N_A, N_D, R=1000, plot=False):
    # if plot:
    #     plt.figure()
    N_A_won = 0
    for i in range(R):
        N_A_won += simulateWar(N_A, N_D)

    # plt.show()

    return N_A_won/R   # returns probability that attacker wins given N_A attacking pieces and N_D defending pieces


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("N_A", type=str, help="number of attacking pieces")
    parser.add_argument("N_D", type=str, help="number of defending pieces")
    parser.add_argument("R", type=str, help="number of simulated wars")

    args = parser.parse_args()
    N_Attackers = int(args.N_A)
    N_Defenders = int(args.N_D)
    R = int(args.R)

    probfrac = simulateWars(N_Attackers, N_Defenders, R=R, plot=False)
    print("Probability of attacker winning with {} pieces against defender with {} pieces".format(N_Attackers, N_Defenders) + " is {}%.".format(probfrac*100))
