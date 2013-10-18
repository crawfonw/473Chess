def parse_string(s):
    board = []
    max_row_length = 0
    for row in s.strip().splitlines():
        row = row.split()
        pieces = []
        for piece in row:
            pieces.append(piece != '*' and piece or None)
        board.append(pieces)
        row_length = len(row)
        if row_length > max_row_length:
            max_row_length = row_length
    for row in board:
        while len(row) < max_row_length:
            row.append(None)
    return board

def print_board(board):
    for row in board:
        for piece in row:
            print piece is not None and piece or '*',
        print

def get_empty_locs(board):
    empty_locs = []
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece is None:
                empty_locs.append((r, c))
    return empty_locs

def get_loc(board, piece):
    for r, row in enumerate(board):
        for c, piece_ in enumerate(row):
            if piece == piece_:
                return (r, c)
    return (-1, -1)

def manhattan_dist(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

def is_in_correct_loc(initial, final, piece):
    return manhattan_dist(get_loc(initial, piece), get_loc(final, piece)) == 0

def get_possible_next_locs(initial, initial_loc):
    possible_next_locs = []
    for empty_loc in get_empty_locs(initial):
        if manhattan_dist(initial_loc, empty_loc) == 1:
            possible_next_locs.append(empty_loc)
    return possible_next_locs

def copy_board(board):
    copy = []
    for row in board:
        row_copy = []
        for piece in row:
            row_copy.append(piece)
        copy.append(row_copy)
    return copy

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

def bfs(piece, initial, final):
    #initilize everything
    unexplored = Queue()
    source = get_loc(initial, piece)
    dest = get_loc(final, piece)
    visited = []
    goal_found = None
    path = {}

    #push the root onto queue
    path[source] = None
    unexplored.enqueue(source)

    #ready, set, search
    while not unexplored.is_empty():
        curr = unexplored.dequeue()
        if curr == dest:
            bfs_path = [curr]
            i = path[curr]
            while i is not None:
                bfs_path.append(i)
                i = path[i]
            goal_found = len(bfs_path) - 1
            break
        else:
            #not goal, so put each never visited child node on the queue
            for next_move in get_possible_next_locs(initial, curr):
                if next_move not in visited:
                    path[next_move] = curr
                    visited.append(next_move)
                    unexplored.enqueue(next_move)
    if goal_found:
        return goal_found # return bfs_path too?
    else:
        return INF

def get_pieces_in_wrong_locs(initial, final):
    pieces_in_wrong_locs = []
    for row in initial:
        for piece in row:
            if piece is not None and not is_in_correct_loc(initial, final, piece):
                pieces_in_wrong_locs.append(piece)
    return pieces_in_wrong_locs
