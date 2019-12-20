import numpy as np
import random
from scipy import ndimage

board = np.zeros([4,4])

def make_move(direction):
    oldboard = np.copy(board)
    alreadymerged = []
    if(direction == "w"):        
        for z in range(3): 
            for i in range(1,4,1):
                for j in range(4):
                    height = i
                    while(height>0):
                        if(board[i-1][j] == 0):
                            board[i-1][j] = board[i][j]  
                            board[i][j] = 0
                            
                        elif(board[i-1][j] == board[i][j] and (str(i-1) + "," + str(j)) not in alreadymerged and (str(i) + "," + str(j)) not in alreadymerged):
                            board[i-1][j]*=2
                            board[i][j] = 0
                            alreadymerged.append(str(i-1) + "," + str(j))
                            alreadymerged.append(str(i) + "," + str(j))
                            
                        height-=1
                            
                    
    
    if(direction == "s"):        
        for z in range(3):   
            for i in range(3,-1,-1):
                for j in range(4):
                    height = i
                    while(height<3):
                        if(board[i+1][j] == 0):
                            board[i+1][j] = board[i][j]  
                            board[i][j] = 0
                            
                        elif(board[i+1][j] == board[i][j] and (str(i) + "," + str(j)) not in alreadymerged and (str(i+1) + "," + str(j)) not in alreadymerged):
                            board[i+1][j]*=2
                            board[i][j] = 0
                            alreadymerged.append(str(i) + "," + str(j))
                            alreadymerged.append(str(i+1) + "," + str(j))
                            
                        height+=1
                        
    
    if(direction == "a"):        
        for z in range(3):   
            for i in range(4):
                for j in range(4):
                    height = j
                    while(height>0):
                        if(board[i][j-1] == 0):
                            board[i][j-1] = board[i][j]  
                            board[i][j] = 0
                            
                        elif(board[i][j-1] == board[i][j] and (str(j) + "," + str(i)) not in alreadymerged and (str(j-1) + "," + str(i)) not in alreadymerged):
                            board[i][j-1]*=2
                            board[i][j] = 0
                            alreadymerged.append(str(j) + "," + str(i))
                            alreadymerged.append(str(j-1) + "," + str(i))
                            
                        height-=1
    
    if(direction == "d"):        
        for z in range(3):   
            for i in range(4):
                for j in range(4):
                    height = j
                    while(height<3):
                        if(board[i][j+1] == 0):
                            board[i][j+1] = board[i][j]  
                            board[i][j] = 0
                            
                        elif(board[i][j+1] == board[i][j] and (str(j) + "," + str(i)) not in alreadymerged and (str(j+1) + "," + str(i)) not in alreadymerged):
                            board[i][j+1]*=2
                            board[i][j] = 0
                            alreadymerged.append(str(j) + "," + str(i))
                            alreadymerged.append(str(j+1) + "," + str(i))
                            
                        height+=1

    if(len(np.where(board.reshape(-1) == 0)[0])>0 and not np.array_equal(board,oldboard)):
        spawn_number()
    
def moves_available():
    for i in range(3):
        for j in range(3):
            if(board[i][j] == board[i][j+1] or board[i][j] == board[i+1][j]):
                return(True)
    return(False)
    

def spawn_number():
    free_cells = np.where(board.reshape(-1) == 0)[0]
    if(len(free_cells) == 0 and not moves_available()):
        print("Game over!")
    else:
        
        rand = random.randint(0,len(free_cells)-1)

        if(random.random()<0.9):
            board.reshape(-1)[free_cells[rand]] = 2
        else:
            board.reshape(-1)[free_cells[rand]] = 4
    return(len(free_cells))  


free_cells = spawn_number()
while(free_cells > 0):
    print(board)
    direction = input()
    make_move(direction)