import sys
import time
import os
from PIL import Image
directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]


class Node:
    def __init__(self, coord):
        self.coord = coord
        self.prev = None


def BFS(maze):
    visited = [[False] * maze.cols for _ in range(maze.rows)]
    start = Node(maze.get_start_coord())
    end = Node(maze.get_end_coord())
    queue = [start]
    visited[start.coord[0]][start.coord[1]] = True
    while queue and queue[0].coord != end.coord:
        cur_node = queue.pop(0)
        for d in directions:
            new_coord = (cur_node.coord[0] + d[0], cur_node.coord[1] + d[1])
            if maze.is_valid_point(new_coord, visited):
                new = Node(new_coord)
                new.prev = cur_node
                queue.append(new)
                visited[new_coord[0]][new_coord[1]] = True
    if queue:
        return queue[0]
    else:
        raise IndexError


def DFS(maze):
    visited = [[False] * maze.cols for _ in range(maze.rows)]
    start = Node(maze.get_start_coord())
    end = Node(maze.get_end_coord())
    queue = [start]
    visited[start.coord[0]][start.coord[1]] = True
    while queue and queue[0].coord != end.coord:
        cur_node = queue.pop(0)
        for d in directions:
            new_coord = (cur_node.coord[0] + d[0], cur_node.coord[1] + d[1])
            if maze.is_valid_point(new_coord, visited):
                new = Node(new_coord)
                new.prev = cur_node
                queue.insert(0, new)
                visited[new_coord[0]][new_coord[1]] = True
    if queue:
        return queue[0]
    else:
        raise IndexError


class Maze:
    def __init__(self, im):
        self.cols = im.size[0]
        self.rows = im.size[1]
        seq_data = list(im.getdata(0))
        self.grid = []
        idx = 0
        for i in range(0, self.rows):
            temp = []
            for j in range(self.cols):
                temp.append(seq_data[idx])
                idx += 1
            self.grid.append(temp)

    def get_start_coord(self):
        for i in range(1, self.cols-1):
            if self.grid[0][i] > 0:
                return 0, i
        raise IOError

    def is_valid_point(self, coord, visited):
        coord_val = 0 <= coord[0] < self.rows and 0 <= coord[1] < self.cols
        visited_val = not visited[coord[0]][coord[1]]
        data_val = self.grid[coord[0]][coord[1]] > 0
        return data_val and visited_val and coord_val

    def get_end_coord(self):
        for i in range(1, self.cols-1):
            if self.grid[self.rows-1][i] > 0:
                return self.rows-1, i
        raise IOError


def get_filename(name):
    if not os.path.isdir('solved'):
        os.mkdir('solved')
    idx_slash = name.rfind('/')
    idx_dot = name.find('.')
    return "solved" + name[idx_slash:idx_dot] + "_solved" + name[idx_dot:]


def draw_path(im, end, name):
    im = im.convert('RGB')
    impixels = im.load()

    node_itr = end
    while node_itr:
        impixels[node_itr.coord[::-1]] = (255, 0, 0)
        node_itr = node_itr.prev

    output_file = get_filename(name)
    im.save(output_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Command line format is python3 main.py <name of file>")
        exit()
    try:
        im = Image.open(sys.argv[1])
    except IOError:
        print("Could not open file %s" % sys.argv[1])
        exit()

    maze = Maze(im)

    start = time.time()
    end = BFS(maze)
    done = time.time()
    print("time elapsed for BFS: %.2f seconds" % (done-start))

    start = time.time()
    end = DFS(maze)
    done = time.time()
    print("time elapsed for DFS: %.2f seconds" % (done-start))

    draw_path(im, end, sys.argv[1])


