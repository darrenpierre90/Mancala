

class Action:
    def __init__(self,tuple:postion,clockwise,skip):
        self.position=position
        self.clockwise=clockwise
        self.skip=skip

class Node:
    def __init__(self,action,state,value):
        self.action=action
        self.state=state
        self.value=value
def minimax(position, depth, alpha, beta, maximizingPlayer)
    if depth == 0 or game over in position
        return static evaluation of position
 
    if maximizingPlayer
        maxEval = -infinity
        for each child of position
            eval = minimax(child, depth - 1, alpha, beta false)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha
                break
        return maxEval
 
    else
        minEval = +infinity
        for each child of position
            eval = minimax(child, depth - 1, alpha, beta true)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha
                break
        return minEval



def min():
    pass

def max():
    pass