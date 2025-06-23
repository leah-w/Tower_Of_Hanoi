#hanoi graph
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

#get number of disks
def numDisks(heights):
  num = 0
  n = len(heights)
  for i in range(n):
    if( num < heights[i]):
      num = heights[i]
  return num

#all disk on first peg
def generateStartState(pegs, disks):
    start_state = [0] * disks
    for i in range(disks):
        start_state[i] = 0
    return tuple(start_state)

#All disks on last peg
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
    for i in range(num_pegs):
        if top_disks[i] != -1:  # There is a disk to move on peg i
            for j in range(num_pegs):
                if i != j and len(pegs[j]) < heights[j]:
                    if top_disks[j] == -1 or top_disks[i] < top_disks[j]:
                        new_state = list(state)
                        new_state[top_disks[i]] = j
                        moves.append(tuple(new_state))
                        #add_edge(edges, (state, new_state))

    return moves

def hanoi(start_state, target_state, num_pegs, heights):
    queue = deque([(start_state, [])])
    visited = set()
    visited.add(start_state)

    while queue:
        current_state, path = queue.popleft()

        if current_state == target_state:
            return path

        for next_state in generateMoves(current_state, num_pegs, heights):
            if next_state not in visited:
                #print(next_state)
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
                add_edge(edges, (current_state, next_state))

    return None

def draw_graph(edges):
    G = nx.Graph()
    
    for edge in edges:
        G.add_edge(str(edge[0]), str(edge[1]))
    
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue',font_size=5)
    labels = {node: node for node in G.nodes()}
    #nx.draw_networkx_labels(G, pos, labels, font_size=10)
    plt.show()


def add_edge(edges, new_edge):
    if new_edge not in edges and (new_edge[1], new_edge[0]) not in edges:
        edges.append(new_edge)

edges = [] #set()
heights = (4,1,1,4) # max height/number of disks allowed for each peg
num_pegs = len(heights)
disks = numDisks(heights)
start_state = generateStartState(num_pegs, disks)  # All disks on first peg
target_state = generateEndState(num_pegs, disks)  # All disks on last peg

path = hanoi(start_state, target_state, num_pegs, heights)

draw_graph(edges)

