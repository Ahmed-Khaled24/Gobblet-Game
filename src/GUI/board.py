class Goblet_Board:
    def __init__(self):
        self.board = [
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]],
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]],
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]],
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]]
              ]


    def place(self,loc,player,size):
        ok = True 
        if self.getPlayer((loc[0],loc[1])) != 'n':
            ok = False
            if sum(self.getPlayer((loc[0],i)) == player for i in range(4)) == 3:
                ok = True
            if sum(self.getPlayer((i,loc[1])) == player for i in range(4)) == 3:
                ok = True
            # Check diagonal for 3 cups
            if loc[0] == loc[1] and sum(self.getPlayer((i,i)) == player for i in range(4)) == 3:
                ok = True
            # Check diagonal for 3 cups
            if loc[0] + loc[1] == 3 and sum(self.getPlayer((3-i,i)) == player for i in range(4)) == 3:
                ok = True
        if not(ok):
            raise Exception
        if size <= self.board[loc[0]][loc[1]][1]:
            raise Exception
        if ok:
            self.board[loc[0]][loc[1]].append(size)
            self.board[loc[0]][loc[1]][0].append(player)
        print("The board after the move is:")
        for col in self.board:
                print(col)
        print(player)
        return ok


        
    def getPlayer(self,pos):
        p = self.board[pos[0]][pos[1]][0]
        return p[-1]

    def getSize(self,pos):
        return self.board[pos[0]][pos[1]][-1]

    def move(self,prev_pos,new_pos,player):
        if (self.board[new_pos[0]][new_pos[1]][-1] >= self.board[prev_pos[0]][prev_pos[1]][-1]):
             raise Exception("Placing smaller cup on position")
        self.board[new_pos[0]][new_pos[1]].append(self.board[prev_pos[0]][prev_pos[1]].pop())
        self.board[prev_pos[0]][prev_pos[1]][0].pop()
        self.board[new_pos[0]][new_pos[1]][0].append(player)

    def check_winner(self):
    # Check rows
      for row in self.board:
        if all(cell[0][-1] == 'R' for cell in row):
            return 'R'
        elif all(cell[0][-1] == 'B' for cell in row):
            return 'B'
      
    # Check columns
      for col in range(len(self.board[0])):
        if all(self.board[row][col][0][-1] == 'R' for row in range(len(self.board))):
            return 'R'
        elif all(self.board[row][col][0][-1] == 'B' for row in range(len(self.board))):
            return 'B'

    # Check diagonals
      if all(self.board[i][i][0][-1] == 'R' for i in range(len(self.board))):
        return 'R'
      elif all(self.board[i][i][0][-1] == 'B' for i in range(len(self.board))):
        return 'B'
      if all(self.board[i][len(self.board)-1-i][0][-1] =='R' for i in range(len(self.board))):
        return 'R'
      elif all(self.board[i][len(self.board)-1-i][0][-1] == 'B' for i in range(len(self.board))):
        return 'B'
        