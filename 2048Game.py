import numpy as np
import random

board = np.zeros([4,4])

def make_move(direction, free_spaces):
    if(direction == "w"):
        for i in range(1,4,1):   
            for j in range(4):
                if(board[i-1][j] == 0):
                    board[i-1][j] = board[i][j]  
                    board[i][j] = 0
                elif(board[i-1][j] == board[i][j]):
                    board[i-1][j]*=2
                    board[i][j] = 0

def spawn_number():
    print(np.flatnonzero(board))
    rand = random.randint(0,len(np.flatnonzero(board)))
    if(random.random()<0.9):
        board.reshape(-1)[rand] = 2
    else:
        board.reshape(-1)[rand] = 4
    
    


free_spaces = 16
while(free_spaces > 0):
    
    spawn_number()
    print(board)
    direction = input("Make move")
    make_move(direction, free_spaces)
    free_spaces-=1
    