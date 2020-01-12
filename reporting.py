from termcolor import colored
import matplotlib.pyplot as plt
import pandas as pd
import time;
import numpy as np
# =============================================================================
#     Scores
# =============================================================================
def plot_boxes(data, title = "", *args, **kwargs):
    fig, ax = plt.subplots()
    if title:
        ax.set_title(title)
    
    ax.boxplot(data, *args, **kwargs)

def plot_table(df):
    plt.rcParams["figure.figsize"] = (12, 12)
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center'
)
    table.set_fontsize(24)
    fig.tight_layout()
    plt.show()

### Finish this
def calculate_moves_total(moves):
    total = 0
    for direction, value in moves.items():
        total += value
    return total

def calculate_move_direction_percentage(moves, total):
    percentage  = []
    for direction, value in moves.items():
        percentage.append((direction, str(round(value / total, 2)) + '%'))
    return percentage
 
def plot_game_reports(data, save_csv = True, add_csv_suffix = True, csv_filename = './data/game_report{}.csv'):    
    df = pd.DataFrame(data, columns=['Moves', 'Score', 'Time', 'Mean Time Per Move', 'Did Win', 'Highest Tile', 'Board'])
    if save_csv:
        suffix = ''
        if add_csv_suffix:
            suffix += ('_' + str(time.time()))

        df.to_csv(csv_filename.format(suffix), index=False)
    
    # Plot table
    plot_table(df)
    
    plot_boxes([df['Score'].values], 'Score', labels=['NN scores'])
    # Score for the best game
    best_moves, best_score, best_time, best_mean, didWin, highest_tile, best_board = df.iloc[df['Score'].idxmax()]

    print('================ Best ====================')
    print('Best score: {}'.format(best_score))
    print('Moves: {}'.format(best_moves))
    total_moves = calculate_moves_total(best_moves)
    print('Moves percentage: {}'.format(calculate_move_direction_percentage(best_moves, total_moves)))
    print('Time taken: {}'.format(float(best_time)))
    print('Highest tile: {}'.format(highest_tile))
    print('Highest tile reached {} times'.format(len(df[df['Highest Tile'] == df['Highest Tile'].max()]))) 
    print('Board', np.array(best_board).reshape(4, 4))
    print('==========================================')
    worst_moves, worst_score, worst_time, worst_mean, didWin, worst_highest_tile, worst_board = df.iloc[df['Score'].idxmin()]
    # Score for the worst game
    print('================ Worst ===================')
    print('Worst score: {}'.format(worst_score))
    print('Moves: {}'.format(worst_moves))
    total_moves = calculate_moves_total(worst_moves)
    print('Moves percentage: {}'.format(calculate_move_direction_percentage(worst_moves, total_moves)))
    print('Time taken: {}'.format(float(worst_time)))
    print('Board', np.array(worst_board).reshape(4, 4))
    print('==========================================')

    wins = len(df.loc[df['Did Win'] == True])
    loses = len(df.loc[df['Did Win'] == False])
    print('Total games: {}'.format(len(data)))
    print('Average score: {}'.format(df['Score'].mean()))
    print('Wins: {}'.format(wins))   
    print('Percentage wins: {}'.format(str(round(didWin / (loses + wins) * 100, 2)) + '%'))
    print('Loses: {}'.format(loses))
    print('Percentage loses: {}'.format(str(round(loses / (loses + wins) * 100, 2)) + '%'))
    print('Highest Tile: {}'.format(worst_highest_tile))
    print('Worst score minimum tile count: {}'.format(len(df[df['Highest Tile'] == df['Highest Tile'].min()])))
    print('==========================================')  
    


def beautify_print(board, color=True):
    """
    Prints the board in a prettier way.
    params:
        board: 4x4 np array representing the board.
    """

    color_dict = {0: "red", 2: "green", 4: "yellow", 8: "blue", 16: "magenta", 32: "cyan", 64: "green",
                  128: "yellow", 256: "blue", 512: "magenta", 1024: "cyan", 2048: "green", 5096: "yellow"}
    print("==================")
    for i in range(4):
        print("|", end=" ")
        for j in range(3):
            try:
                if color == 'True':
                    print(
                        colored(str(int(board[i][j])), color_dict[int(board[i][j])]), end=" | ")
                else:
                    print(str(int(board[i][j])), end=" | ")
            except Exception as e:
                print(e)
                print(board[i][j], end=" | ")
        try:
            if color is 'True':
                print(colored(str(int(board[i][3])),
                              color_dict[int(board[i][3])]), end=" |\n")
            else:
                print(str(int(board[i][3])) , end=" |\n")
        except:
            print(board[i][3], end=" |\n")
        print("==================")

def get_scores(scores):
    final_scores = {"w":[0,0], "a":[0,0], "s":[0,0], "d":[0,0],}
    for score in scores:
              final_scores[score[0]][0] += score[1]
              final_scores[score[0]][1] += 1

    best_score = 0
    for i in final_scores:
        try:
            final_scores[i][0] /= final_scores[i][1]
        except:
            final_scores[i][0] = 0
        if final_scores[i][0] > best_score:
            best_score = final_scores[i][0]
            best_move = i
    return (best_score, final_scores)