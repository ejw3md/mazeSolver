import sys
import time
import os
from PIL import Image
from maze import Maze, Cell

directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def BFS(maze):
    visited = [[False] * maze.cols for _ in range(maze.rows)]
    start = Cell(maze.get_start_coord())
    end = Cell(maze.get_end_coord())
    queue = [start]
    visited[start.coord[0]][start.coord[1]] = True
    while queue and queue[0].coord != end.coord:
        cur_cell = queue.pop(0)
        for d in directions:
            new_coord = (cur_cell.coord[0] + d[0], cur_cell.coord[1] + d[1])
            if maze.is_valid_point(new_coord, visited):
                new = Cell(new_coord)
                new.prev = cur_cell
                queue.append(new)
                visited[new_coord[0]][new_coord[1]] = True
    if queue:
        return queue[0]
    else:
        raise IndexError


def DFS(maze):
    visited = [[False] * maze.cols for _ in range(maze.rows)]
    start = Cell(maze.get_start_coord())
    end = Cell(maze.get_end_coord())
    queue = [start]
    visited[start.coord[0]][start.coord[1]] = True
    while queue and queue[0].coord != end.coord:
        cur_cell = queue.pop(0)
        for d in directions:
            new_coord = (cur_cell.coord[0] + d[0], cur_cell.coord[1] + d[1])
            if maze.is_valid_point(new_coord, visited):
                new = Cell(new_coord)
                new.prev = cur_cell
                queue.insert(0, new)
                visited[new_coord[0]][new_coord[1]] = True
    if queue:
        return queue[0]
    else:
        raise IndexError


def get_filename(name):
    if not os.path.isdir('solved'):
        os.mkdir('solved')
    idx_slash = name.rfind('/')
    idx_dot = name.find('.')
    return "solved" + name[idx_slash:idx_dot] + "_solved" + name[idx_dot:]


def draw_path(im, end, name):
    im = im.convert('RGB')
    impixels = im.load()

    cell_itr = end
    while cell_itr:
        impixels[cell_itr.coord[::-1]] = (255, 0, 0)
        cell_itr = cell_itr.prev

    output_file = get_filename(name)
    im.save(output_file)


def main():
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
    print("time elapsed for BFS: %.2f seconds" % (done - start))

    start = time.time()
    end = DFS(maze)
    done = time.time()
    print("time elapsed for DFS: %.2f seconds" % (done - start))

    draw_path(im, end, sys.argv[1])


if __name__ == '__main__':
    main()
