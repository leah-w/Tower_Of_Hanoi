#hanoi motifyed
#three lists with one max height of celing(n/2)
#min lenght n-1
#towers of hanoi 2 shorter extra towers -> must be combined height n-1 
#in order to move the largest (n disk) all other n-1 disks must be moved to the some other peg 
# and that peg must have height n-1 to be able to hold the other n-1 disks. If the auxillury tower were 
# less than height n-1 atleast on disk that is less that n must be on the destination peg. The nth disk cannot 
# move on top of that disk because it is less than n. 

import math
from collections import deque

#all disk on first peg
def generateStartState(pegs, disks):
    start_state = [0] * disks
    for i in range(disks):
        start_state[i] = 0
    return tuple(start_state)

#all disks on last peg
def generateEndState(num_pegs, disks):
    end_state = [0] * disks
    for i in range(disks):
        end_state[i] = num_pegs - 1
    return tuple(end_state)

def generateMoves(state, num_pegs, heights):
    n = len(state)
    pegs = [[] for _ in range(num_pegs)]

    # Distribute disks on the pegs according to the state tuple
    for i in range(n):
        pegs[state[i]].append(i)
    
    # Determine the top disk on each peg
    top_disks = [-1] * num_pegs
    for i in range(num_pegs):
        if pegs[i]:
            top_disks[i] = pegs[i][0]

    moves = []
    # Generate possible moves
    for i in range(num_pegs):
        if top_disks[i] != -1:  # There is a disk to move on peg i
            for j in range(num_pegs):
                if i != j and len(pegs[j]) < heights[j]:
                    if top_disks[j] == -1 or top_disks[i] < top_disks[j]:
                        new_state = list(state)
                        new_state[top_disks[i]] = j
                        moves.append(tuple(new_state))

    return moves

def hanoi(start_state, target_state, num_pegs, heights):
    queue = deque([(start_state, [])])
    visited = set()
    visited.add(start_state)

    while queue:
        current_state, path = queue.popleft()

        if current_state == target_state:
            return [start_state] + path

        for next_state in generateMoves(current_state, num_pegs, heights):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))

    return None


def statesToMoves(states):
    moves = []    
    #states = states.insert(1,start_state)
    for i in range(len(states) - 1):
        current_state = states[i]
        next_state = states[i + 1]
        
        for disk in range(len(current_state)):
            if current_state[disk] != next_state[disk]:
                move = (current_state[disk], next_state[disk])
                moves.append(move)
                break
                
    return moves


num_pegs = 4 
disks = 5

start_state = generateStartState(num_pegs, disks)  # All disks on first peg
target_state = generateEndState(num_pegs, disks)  # All disks on last peg
#numSteps = 0; 

for i in range(1, disks+1):
    for j in range(1, i+1):
        heights = (disks ,j, i, disks)
        path = hanoi(start_state, target_state, num_pegs, heights)
        print("path with heights ",heights, ":")
        if(path == None):
            print("No solution")
        else:
            numSteps = len(path)
            print("steps:",numSteps-1)

#num_pegs = 4  disks = 15
#heights = (5,1,1,5) # max height/number of disks allowed for each peg 
#num_pegs = len(heights)
#disks = heights[0]
