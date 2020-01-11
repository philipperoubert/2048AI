from termcolor import colored
import matplotlib.pyplot as plt
import pandas as pd
    
# =============================================================================
#     Scores
# =============================================================================

def plot_table(df):
    plt.rcParams["figure.figsize"] = (8, 8)
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center'
)
    fig.tight_layout()
    plt.show()

### Finish this
def calculate_moves_total(moves):
    total = 0
    for direction, value in moves.items():
        print('move', direction, value)
        total += value
    return total

def calculate_move_direction_percentage(moves, total):
    percentage  = []
    for direction, value in moves.items():
        percentage.append((direction, str(round(value / total, 2)) + '%'))
    return percentage
    
# total = calculate_moves_total({
#     'w': 25,
#     'a': 50
# })
# perc = calculate_move_direction_percentage({
#     'w': 25,
#     'a': 50
# }, total)

# print('total', total)
# print('perc', perc)
        
def plot_game_reports(data):    
    df = pd.DataFrame(data, columns=['Moves', 'Score', 'Time', 'Mean Time Per Move'])    
    plot_table(df)
    best_moves, best_score, best_time, best_mean = df.iloc[df['Score'].argmax()]
    print('================ Best ====================')
    print('Best score: {}'.format(best_score))
    print('Moves: {}'.format(best_moves))
    print('Time taken: {}'.format(float(best_time)))
    print('==========================================')
    worst_moves, worst_score, worst_time, worst_mean = df.iloc[df['Score'].argmin()]
    print('================ Worst ===================')
    print('Worst score: {}'.format(worst_moves))
    print('Moves: {}'.format(worst_moves))
    print('Time taken: {}'.format(float(worst_time)))
    print('==========================================')
    print('=============== Number of moves ==========')
    


def beautify_print(board):
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
                print(
                    colored(str(int(board[i][j])), color_dict[int(board[i][j])]), end=" | ")
            except:
                print(board[i][j], end=" | ")
        try:
            print(colored(str(int(board[i][3])),
                          color_dict[int(board[i][3])]), end=" |\n")
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