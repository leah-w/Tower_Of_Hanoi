#hanoi animate
from manim import *
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

def generateStates(state, num_pegs, heights):
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

    states = []
    # Generate possible moves
    for i in range(num_pegs):
        if top_disks[i] != -1:  # There is a disk to move on peg i
            for j in range(num_pegs):
                if i != j and len(pegs[j]) < heights[j]:
                    if top_disks[j] == -1 or top_disks[i] < top_disks[j]:
                        new_state = list(state)
                        new_state[top_disks[i]] = j
                        states.append(tuple(new_state))

    return states

def hanoi(start_state, target_state, num_pegs, heights):
    queue = deque([(start_state, [])])
    visited = set()
    visited.add(start_state)

    while queue:
        current_state, path = queue.popleft()

        if current_state == target_state:
            return [start_state] + path

        for next_state in generateStates(current_state, num_pegs, heights):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))

    return [start_state] + path

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

#moves 
#num_pegs = 4  disks = 15
heights = (5,2,5,5) # max height/number of disks allowed for each peg 
num_pegs = len(heights)
disks = heights[0]

start_state = generateStartState(num_pegs, disks)  # All disks on first peg
target_state = generateEndState(num_pegs, disks)  # All disks on last peg
path = hanoi(start_state, target_state, num_pegs, heights)
moves = statesToMoves(path) 
    

class TowerOfHanoi(Scene):
    def __init__(self, num_disks=5, num_pegs = 4, moves = moves, heights = heights, **kwargs):
        super().__init__(**kwargs)
        self.num_disks = num_disks
        self.num_pegs = num_pegs
        self.pegs = [[] for _ in range(num_pegs)]  
        self.moves = moves or []
        self.heights = heights 

    #moves
    def moveDisk(self, source, target, pegGroup,animate):
        print(source)
        disk = self.pegs[source][-1]
        
        if(animate):
            self.play(disk.animate.move_to(pegGroup[source].get_top() + np.array([0, 0.5, 0]))) #up
            self.play(disk.animate.move_to(pegGroup[target].get_top() + np.array([0, 0.5, 0]))) #move
            self.play(disk.animate.move_to(pegGroup[target].get_bottom() + (UP * 0.5) + np.array([0, len(self.pegs[target]) * 0.55, 0]))) #down
        else:
            #self.play(disk.animate.move_to(pegGroup[target].get_bottom() + (UP * 0.5) + np.array([0, len(self.pegs[target]) * 0.55, 0])), 
                      #run_time = 0.1)
            self.wait(0.25)        
            self.add(disk.move_to(pegGroup[target].get_bottom() + (UP * 0.5) + np.array([0, len(self.pegs[target]) * 0.55, 0])))
            self.wait(0.25) 

        self.pegs[source].remove(disk)
        self.pegs[target].append(disk)
 
    def construct(self):
        #write heights              
        wordGroup = Group()
        for i in heights:
            h = Text(str(i)).set_color(WHITE)
            #h.next_to(pegGroup[i], DOWN)
            wordGroup.add(h)  
        self.add(wordGroup.arrange(RIGHT, buff = 3).to_edge(DOWN))  

        #make pegs 
        pegGroup = Group()
        heightMax = 5
        heightMod = 0
        for i in range(self.num_pegs):
            #height_mod = heights[0]/heights[i]
            #size = heightMax * heightMod
            peg = Rectangle(stroke_width = 0, height = 5 , width = 0.25).set_fill(DARK_BROWN,1)
            pegGroup.add(peg)
        self.add(pegGroup.arrange(buff=3, aligned_edge = DOWN))
        
        # make disks 
        diskGroup = Group()
        colors = [BLUE, YELLOW, RED, GREEN, PURPLE] 
  
        total_width = 6  
        sum_of_n = self.num_disks * (self.num_disks + 1) / 2
        width_multiplier = total_width / sum_of_n

        for i in reversed(range(self.num_disks)):
            size = (i+1) * width_multiplier
            disk = Rectangle(height = 0.5, width = size, color=colors[i % len(colors)], fill_opacity=1)   
            diskGroup.add(disk)

        pos = pegGroup[0].get_bottom() + (UP) + np.array([0, 0.75, 0])
        self.add(diskGroup.arrange(UP, buff = 0.1).move_to(pos)) 

        #labels later
        numGroup = Group()
        for i in reversed(range(self.num_disks)):
            h = Text(str(i+1)).set_color(BLACK)
            h.move_to(diskGroup[i].get_center())
            numGroup.add(h)         
        #self.add(numGroup)

        #put all disks on list for first peg 
        for disk in diskGroup:
            self.pegs[0].append(disk) 
             
        #move disks according to the provided moves
        animate = True
        if len(self.moves) > 10:
                animate = False
        for move in self.moves:
            source , target = move
            self.moveDisk(source, target, pegGroup, animate)  
        self.wait(0.2)




class FourColoredPegs(Scene):    
    def construct(self):
        #colors = [BLUE, YELLOW, RED, GREEN]
        peg_1 = Rectangle(color = BLUE, stroke_width = 10, height = 5, width = 0.75 )
        #peg_1.stretch_to_fit_height(5)
        #peg_1.stretch_to_fit_width(0.75)
        #peg_1.set_stroke(BLUE, width=10)
       
        peg_2 = Rectangle(color = YELLOW, stroke_width = 10, height = 5, width = 0.75)        
        peg_3 = Rectangle(color = RED, stroke_width = 10, height = 5, width = 0.75)
        peg_4 = Rectangle(color = GREEN, stroke_width = 10, height = 5, width = 0.75)
           
        pegGroup = Group(peg_1, peg_2, peg_3, peg_4).arrange(buff=2)
        self.add(pegGroup)

class DivideRectangles(Scene):
    def construct(self):
        num_rectangles = 5  # Change this value to the number of rectangles you want
        total_height = 6  # Total height of the combined rectangles
        total_width = 2  # Width of each rectangle

        # Calculate the sum of the first n natural numbers
        sum_of_n = num_rectangles * (num_rectangles + 1) / 2

        # Calculate the base height multiplier
        height_multiplier = total_height / sum_of_n

        rectangles = []
        current_bottom = -total_height / 2

        for i in range(1, num_rectangles + 1):
            height = i * height_multiplier
            rect = Rectangle(height=height, width=total_width, color=WHITE, fill_opacity=0.5)
            rect.move_to(ORIGIN + UP * (current_bottom + height / 2))
            rectangles.append(rect)
            self.add(rect)
            current_bottom += height

        self.wait(2)

       

        