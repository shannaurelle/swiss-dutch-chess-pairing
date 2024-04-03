# experimental script for improved swiss ranking with dutch pairing
# Author: Shann Aurelle Ripalda
import networkx as nx
from mwmatching import maxWeightMatching

# FIDE plainly guarantees two rules:
# A1: players should have a roughly difference between white and black
# as on the interval [-2,2]
# A2: players should play with other players of roughly equal strength

## constants to remember
N = int(input("Number of Players in the Game: "))
# C: continue counter (0 for with seeding, 1 for continuing rounds)
C = int(input("Starting round (0 if yes, 1 if no): "))
# R: number of rounds
R = int(input("Round: "))-1
# beta: value for the difference between white and black picks (2 for FIDE)
BETA = 2.0

## arrays for the program

# seed: initial ranking for the players
seed = []
# score: scores for all players
score = []
# rank: sortable list of indexes referring to
# the player v of rank i is equal to rank[i] = v
rank = []
# cd: color difference of player i
cd = []
# prior matches
# matches are in the form (white player, black player)
# while players are numbered 0 to N-1
# examples: 
# player 1 (white) vs player 2 (black) is 0 1
# player 3 (white) vs player 1 (black) is 2 0
prev_pairings = []

# debug printing
print("==== PROGRAM PARAMETERS ====")
print("Number of players: ",N)
print("Round: ",R+1)
print("Starting Round (0 if yes, 1 if not): ",C)
print("Maximum color difference: ",BETA)
if (C == 0):
    print("Starting round ")
    
elif (C == 1):
    print("Continuing round")

seed = [int(i) for i in input("Input the seed of each player ").split(" ")]

if (C == 1):
    score = [int(i) for i in input("Input the score of each player ").split(" ")]
    whites = [int(i) for i in input("Input how many times players took white ").split(" ")]
    blacks = [int(i) for i in input("Input how many times players took black ").split(" ")]
    P = R * (N // 2)
    print("=== PREVIOUS PAIRINGS ===")
    for i in range(P):
        P1, P2 = [int(i) for i in input().split(" ")]
        prev_pairings.append((P1,P2))
    cd = [(white - black) for white,black in zip(whites,blacks)]
    I = [index for index in range(len(score))]
    rank = [index for _,index in sorted(zip(score,I),reverse=True)]
    
print("==== PROGRAM DATA ====")
if(C == 1):
    print("Player: ",end="")
    for p in range(N):
        print(p,end=" ")
    print()
    print("Score: ",end="")
    for s in score:
        print(s,end=" ")
    print()
    print("Color difference: ",end="")
    for diff in cd:
        print(diff,end=" ")
    print()
    print("Rank: ",end="")
    for r in rank:
        print(r,end=" ")
    print()
curr_round = 1 if (R == 0) else (R+1)
print("=== ROUND ",curr_round," ===")
# graph creation
# if initial round, use dutch pairing system
# using the seed divide into two halfs, pair the
# ith element of the first half with the second half

# bye := player which will have a free point this round
bye = 0
# sorted seed has seed j for player i
sorted_seed = sorted((j,i) for i,j in enumerate(seed))
if(C == 0):
    mid = N // 2
    top_half = sorted_seed[:mid]
    bottom_half = sorted_seed[mid:]
    for i,j in zip(top_half,bottom_half):
        player = 1
        print("Player ",i[player]+1,"(White) vs Player ",j[player]+1,"(Black)")
    # pick the player with lowest seed as bye
    if(N % 2 == 1):
        bye = any(i for i in seed if i == max(seed))
        print("Bye: Player ",bye)

# match making
sorted_rank = sorted((rank,player) for player,rank in enumerate(rank))
# edges array with tuples (i,j,w)
# i and j are the players and w is the weight
edges = []
if(C == 1):
    # make an upper triangular adjacency matrix
    for p_A in range(N):
        for p_B in range(p_A,N):
            if(p_A != p_B and (p_A,p_B) not in prev_pairings and abs(cd[p_A] + cd[p_B]) < 2 * BETA):
                # weight computation
                wt = 10000.0 * (-1.0*abs(score[p_A] - score[p_B]))
                wt += 100.0 * (-1.0*abs(cd[p_A] + cd[p_B]))
                # pi function for dutch system
                sg_size = 0.0 if abs(score[p_A] - score[p_B]) > 0 else sum(1.0 for i in score if i == score[p_A])
                wt += -1.0 * abs(sg_size / 2.0 - abs(rank[p_A] - rank[p_B]))**1.01
                edges.append((p_A,p_B,round(wt,2)))
for e in edges:
    print(e)
paths = maxWeightMatching(edges,True)
for i,e in enumerate(paths):
    print(i," ",e)
matched = set()
pairings = []
# this one is for announcing it to the referees
print("=== ROUND,",R+1,"MATCHES ===")
for player_A,player_B in enumerate(paths):
    if((player_A not in matched or player_B not in matched) and player_B != -1):
        if(R % 2 == 0):
            pairings.append((player_B,player_A))
            print("Player ",player_B,"(White) vs Player ",player_A,"(Black)")
        else:
            pairings.append((player_A,player_B))
            print("Player ",player_A,"(White) vs Player ",player_B,"(Black)")
        matched.add(player_A)
        matched.add(player_B)
# a separate printing of numbers for storage in paper
for i,j in pairings:
    print(i," ",j)
        
        







