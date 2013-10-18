'''
Created on Nov 1, 2011

@author: crawfonw
'''

INF = float('inf')

class Queue:
    def __init__(self):
        self.list = []

    def enqueue(self, item):
        self.list.insert(0, item)

    def dequeue(self):
        return self.list.pop()

    def is_empty(self):
        return len(self.list) == 0

'''
def bfs(state):
    #initilize everything
    unexplored = Queue()
    source = state
    visited = []
    goal_found = None

    #push the root onto queue
    unexplored.push(state)

    #ready, set, search
    while not unexplored.is_empty():
        curr = unexplored.pop()
        if state.is_goal_state():
            goal_found = curr
            break
        else:
            #not goal, so put each never visited child node on the queue
            for next_move in state.get_successors():
                if next_move not in visited:
                    visited.append(next_move)
                    unexplored.push(next_move)
    if goal_found:
        return goal_found
    else:
        return INF
'''
