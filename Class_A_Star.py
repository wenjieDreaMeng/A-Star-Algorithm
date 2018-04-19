#########################################################  
class Node_Elem:  
    def __init__(self, parent, x, y, dist):
        self.parent = parent  
        self.x = x  
        self.y = y  
        self.dist = dist  
          
class A_Star:
    def __init__(self, s_x, s_y, e_x, e_y, board_end_x, board_end_y, board_start_x, board_start_y):
        self.s_x = s_x  
        self.s_y = s_y  
        self.e_x = e_x  
        self.e_y = e_y  
          
        self.width = board_end_x - board_start_x + 1
        self.height = board_end_y - board_start_y + 1

        self.barrierList = []
          
        self.open = []  
        self.close = []  
        self.path = []  

    #   set the barrier area
    def setBarrierList(self,barrier_list):
        self.barrierList = barrier_list

    def find_path(self):
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:  
            self.extend_round(p)
            if not self.open:
                return  
            idx, p = self.get_best()
            if self.is_target(p):
                self.make_path(p)  
                return  
            self.close.append(p)
            del self.open[idx]  
              
    def make_path(self,p):  
        while p:
            self.path.append((p.x, p.y))  
            p = p.parent  
          
    def is_target(self, i):  
        return i.x == self.e_x and i.y == self.e_y  
    
    #   Traversing open list, find the minimum point of the value
    def get_best(self):  
        best = None  
        bv = 1000000
        bi = -1  
        for idx, i in enumerate(self.open):  
            value = self.get_dist(i)
            if value < bv:
                best = i  
                bv = value  
                bi = idx  
        return bi, best  
          
    def get_dist(self, i):  
        # F = G + H  
        #   use Manhattan distance 
        return i.dist + ( abs(self.e_x-i.x) + abs(self.e_y-i.y) )
        #   use Euclidean distance
        #   return i.dist + math.sqrt(
        #    (self.e_x-i.x)*(self.e_x-i.x)  
        #    + (self.e_y-i.y)*(self.e_y-i.y))*1.2  
          
    def extend_round(self, p):  
        #   eight direction to find path
        #   xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        #   ys = (-1,-1,-1,  0, 0,  1, 1, 1)  
        
        #   only consider four direction to find path
        xs = (0, -1, 0, 1)
        ys = (-1, 0, 1, 0)  
        for x, y in zip(xs, ys):  
            new_x, new_y = x + p.x, y + p.y  
            if not self.is_valid_coord(new_x, new_y):
                continue  
            node = Node_Elem(p, new_x, new_y, p.dist+self.get_cost(
                        p.x, p.y, new_x, new_y))  
            if self.node_in_close(node):
                continue  
            i = self.node_in_open(node)  
            if i != -1:  
                if self.open[i].dist > node.dist:
                    self.open[i].parent = p
                    self.open[i].dist = node.dist  
                continue  
            self.open.append(node)  
    
    #   The cost of horizontal mobility and vertical mobility is 1, while the cost of diagonal mobility is 1.4
    def get_cost(self, x1, y1, x2, y2):  
        if x1 == x2 or y1 == y2:
            return 1.0  
        return 1.0  
          
    def node_in_close(self, node):  
        for i in self.close:  
            if node.x == i.x and node.y == i.y:  
                return True  
        return False  
          
    def node_in_open(self, node):  
        for i, n in enumerate(self.open):  
            if node.x == n.x and node.y == n.y:  
                return i  
        return -1  
     
    #   Determine whether or not it is in a valid area
    def is_valid_coord(self, x, y):  
        if x < 0 or x >= self.width or y < 0 or y >= self.height:  
            return False

        for i in range(len(self.barrierList)):
            barrier_s_x = self.barrierList[i][0][0]
            barrier_s_y = self.barrierList[i][0][1]
            barrier_e_x = self.barrierList[i][1][0]
            barrier_e_y = self.barrierList[i][1][1]
            # this point is in the barrier,so don't through it
            if (((x - barrier_s_x)*(x - barrier_e_x) <= 0) and ((y - barrier_s_y)*(y - barrier_e_y) <= 0)) == True:
                return False

        return True

    def get_searched(self):  
        l = []  
        for i in self.open:  
            l.append((i.x, i.y))  
        for i in self.close:  
            l.append((i.x, i.y))  
        return l  
          