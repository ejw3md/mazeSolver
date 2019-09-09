class Cell:
    def __init__(self, coord):
        self.coord = coord
        self.prev = None


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

