from itertools import combinations
from copy import deepcopy

from chess import *


i_string = """
A B * D
* * * *
* E G *
F * C H
"""

f_string = """
A B C D
* * * *
* * * *
E F G H
"""


INITIAL = parse_string(i_string)

FINAL = parse_string(f_string)

PIECES = get_pieces_in_wrong_locs(INITIAL, FINAL)

TABLE = {():0}
T = {}
T1 = {}

class Stage:
    def __init__(self, n, initial, final):
        """
        n: number of pieces in the wrong spot
        """
        self.n = n
        self.initial = initial
        self.final = final
        for pieces in combinations(PIECES, n):
            State(pieces, initial, final).minimize()

    def run(self):
        if self.n < len(PIECES):
            Stage(self.n + 1, self.initial, self.final).run()

def exclude(l, v):
    """
    l: list
    v: value to exclude from l
    """
    return [i for i in l if i != v]

class State:
    def __init__(self, pieces, initial, final):
        """
        pieces: a list of pieces in the wrong spot
        """
        self.pieces = pieces
        self.initial = initial
        self.final = final

    def minimize(self):
        temp = []
        f = copy_board(self.final)
        for piece in self.pieces:
            key = tuple(sorted(exclude(self.pieces, piece)))
            i_r, i_c = get_loc(self.initial, piece)
            f_r, f_c = get_loc(self.final, piece)
            f[f_r][f_c] = None
            if f[i_r][i_c] is not None:
                val = INF
            else:
                f[i_r][i_c] = piece
                val = bfs(piece, f, self.final) + TABLE[key]
            T1[(piece, key)] = val
            temp.append(val)
        m = min(temp)
        TABLE[tuple(sorted(self.pieces))] = m
        return m

def in_list(_list):
    for i in _list:
        if i:
            return i

def find_solution_path(i, path=[]):
    minimum = INF
    for j in list_by_length[i]:
        if j[0][0] not in [l[0] for l in path] and not in_list([k in path for k in j[0][1]]) and j[1] < minimum:
            minimum = j[1]
    if minimum == INF:
        return None
    
    for j in list_by_length[i]:
        if j[1] == minimum:
            if i != 0:
                if not in_list([k in path for k in j[0][1]]) and j[0][0] not in [l[0] for l in path]:
                    path.append((j[0][0], get_loc(FINAL, j[0][0])))
                    return find_solution_path(i-1, path)
            else:
                if j[0][0] not in [l[0] for l in path]:
                    path.append((j[0][0], get_loc(FINAL, j[0][0])))
                    return path

boards = Queue()
boards.enqueue((INITIAL, []))

sol = None
while sol is None:
    initial, past_moves = boards.dequeue()
    Stage(1, initial, FINAL).run()

    T2 = list(T1.items())
    T2.sort(key = lambda t: -len(t[0][0])-len(t[0][1]))
    
    list_by_length = []
    for i in range(len(PIECES)):
        list_by_length.append([])
    
    for key, val in T2:
        print key, val
        list_by_length[len(key[0]) + len(key[1]) - 1].append((key, val))
    print
    
    path = []
    i = len(PIECES) - 1
    num_moves = min(list_by_length[-1], key=lambda x: x[1])[1]
    sol = find_solution_path(i, path)
    print sol
    if sol is None:
        for piece in PIECES:
            if T1[(piece, ())] is not INF:
                pos = get_loc(initial, piece)
                moves = get_possible_next_locs(initial, pos)
                for move in moves:
                    new_past_moves = deepcopy(past_moves)
                    new_past_moves.append((piece, move))
                    next = copy_board(initial)
                    next[pos[0]][pos[1]] = None
                    next[move[0]][move[1]] = piece
                    boards.enqueue((next, new_past_moves))
    else:
        num_moves += len(past_moves)
        past_moves.extend(sol)
        sol = past_moves

formatted_sol = []
for piece, move in sol:
    formatted_sol.append('Move %s to %s' % (piece, move))

print 'This board can be reset in %s moves with the following sequence: %s.' % (num_moves, formatted_sol)

