import math  
from Class_A_Star import A_Star,Node_Elem

test_map = []

class MapMatrix:
    def __init__(self,start_x, start_y, end_x, end_y, board_end_x, board_end_y, board_start_x = 0, board_start_y = 0):

        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.board_end_x = board_end_x
        self.board_end_y = board_end_y
        self.board_start_x = board_start_x
        self.board_start_y = board_start_y
        self.width = self.board_end_x - self.board_start_x + 1
        self.height = self.board_end_y - self.board_start_y + 1
        self.barrierList = []
        # Deep Copy
        self.map = [(['.'] * self.width) for i in range(self.height)]
        for i in range(self.width):
            for j in range(self.height):
                if (i == 0 or i == self.width - 1) or (j == 0 or j == self.height-1):
                    self.map[j][i] = '#'

        self.map[start_y][start_x] = 'S'
        self.map[end_y][end_x] = 'E'

    def setBarrierList(self,barrier_list):
        self.barrierList = barrier_list
        for i in range(len(self.barrierList)):
            barrier_s_x = self.barrierList[i][0][0]
            barrier_s_y = self.barrierList[i][0][1]
            barrier_e_x = self.barrierList[i][1][0]
            barrier_e_y = self.barrierList[i][1][1]

            for i in range(barrier_s_x,barrier_e_x+1):
                self.map[barrier_s_y][i] = '#'
                self.map[barrier_e_y][i] = '#'
            for i in range(barrier_s_y,barrier_e_y+1):
                self.map[i][barrier_s_x] = '#'
                self.map[i][barrier_e_x] = '#'

    def print_map(self):
        for line in self.map:
            print ''.join(line)

    def mark_symbol(self,l, s):
        for x, y in l:
            self.map[y][x] = s

    def mark_path(self, l):
        self.mark_symbol(l, '*')

    def mark_searched(self, l):
        self.mark_symbol(l, ' ')

    def find_path(self):

        a_star = A_Star(self.start_x, self.start_y, self.end_x, self.end_y,
                        self.board_end_x, self.board_end_y, self.board_start_x, self.board_start_y)
        a_star.setBarrierList(self.barrierList)
        a_star.find_path()
        searched = a_star.get_searched()
        path = a_star.path
        print "Path:",path
        # self.mark_searched(searched)
        self.mark_path(path)
        self.map[self.start_y][self.start_x] = 'S'
        self.map[self.end_y][self.end_x] = 'E'

if __name__ == "__main__":

    map = MapMatrix(1, 1, 8, 8, 10, 10)
    map.setBarrierList([[(1, 2), (8, 6)]])
    map.print_map()
    map.find_path()
    map.print_map()