import numpy as np
import random
from scipy import ndimage
import os
from termcolor import colored

#creating the board


def make_move(direction, board):
   
    oldboard = np.copy(board) #makes copy of the initial board state
    alreadymerged = [] #coordinates of merged tiles
    if(direction == "w"):    #moving up     
        for z in range(3): #ensures all pieces move as far as they can
            for i in range(1,4,1):
                for j in range(4):
                    height = i
                    while(height>0): #prevents tiles moving off screen.
                        if(board[i-1][j] == 0):
                            board[i-1][j] = board[i][j]  
                            board[i][j] = 0
                            
                        elif(board[i-1][j] == board[i][j] and (str(i-1) + "," + str(j)) not in alreadymerged and (str(i) + "," + str(j)) not in alreadymerged):
                            board[i-1][j]*=2
                            board[i][j] = 0
                            alreadymerged.append(str(i-1) + "," + str(j)) #logs tiles which have merged
                            alreadymerged.append(str(i) + "," + str(j)) #logs tiles which have merged
                            
                        height-=1
                            
                    
    
    if(direction == "s"):    #down    
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
                        
    
    if(direction == "a"):       #left 
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
    
    if(direction == "d"):   #right     
        for z in range(3):   
            for i in range(3,-1,-1):
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
        updated_board = spawn_number(board)
        
        return(updated_board)
    return(board)
    
    
def moves_available(board):
    
    free_cells = np.where(board.reshape(-1) == 0)[0] #list containing indexes of 0's
    
    if(len(free_cells) != 0):
        return(True)
              
    initialboard = np.copy(board)
    initialboard = make_move("w",initialboard)
    initialboard = make_move("s", initialboard)
    initialboard = make_move("a", initialboard)
    initialboard = make_move("d", initialboard)
    
    if(np.array_equal(initialboard,board)):
        print("Should be game over")
        return(False)
    else:
        return(True)
 
    

def spawn_number(board):
        free_cells = np.where(board.reshape(-1) == 0)[0] #list containing indexes of 0's
        if(len(free_cells)>0):
            rand = random.randint(0,len(free_cells)-1) #picks a random free spaces to spawn
            if(random.random()<0.9):
                board.reshape(-1)[free_cells[rand]] = 2 #90% of the time it will spawn a 2
            else:
                board.reshape(-1)[free_cells[rand]] = 4
        return(board) 

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def beautify_print(board):

    color_dict = {0:"red", 2:"green", 4:"yellow", 8:"blue", 16:"magenta", 32:"cyan", 64:"green", 128:"yellow", 256:"blue", 512:"magenta", 1024:"cyan", 2048:"green", 5096:"yellow"}
    cls()
    print("==================")
    for i in range(4):
        print("|", end = " ")
        for j in range(3):
            try:
                print(colored(str(int(board[i][j])), color_dict[int(board[i][j])]), end = " | ")
            except:
                print(board[i][j], end = " | ")
        try:
            print(colored(str(int(board[i][3])), color_dict[int(board[i][3])]), end = " |\n")
        except:
            print(board[i][3], end = " |\n")
        print("==================")		


print("Game starting")
board = np.zeros([4,4])
free_cells = spawn_number(board)
beautify_print(board)
direction = input()
board = make_move(direction, board)
while(moves_available(board)):
    beautify_print(board)
    direction = input()
    board = make_move(direction, board)
beautify_print(board)
print("Game over")