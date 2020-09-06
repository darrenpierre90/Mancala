from termcolor import colored, cprint 
from colorama import Fore, Back, Style
import logging as log 
import random
from copy import deepcopy
from math import inf
FORMAT  ='%(levelname)s:%(message)s'
log.basicConfig(format=FORMAT,level=log.DEBUG)

class Action:
    def __init__(self,position,clockwise,skip):
        self.position=position
        self.clockwise=clockwise
        self.skip=skip
    def __str__(self):
        return(f"{self.position},{self.clockwise},{self.skip}")
    def __eq__(self,other):
        return self.position == other.position and self.clockwise ==other.clockwise  and self.skip == other.skip

class Model:
   
    BLUE_P=[0,2]
    RED_P=[1,3]
    def __init__(self,num_stones):
        if num_stones >6 or num_stones < 0 :
            raise Exception

        else:
            self.board=[num_stones for x in range(6*4)]
            for x in Model.BLUE_P:
                startBoardIndex=x*6
                self.board[startBoardIndex+3]=0
            for x in Model.RED_P:
                startBoardIndex=x*6
                self.board[startBoardIndex+3]=0
            choice=random.choice([True,False])
            self.blueTurn=choice
            player="Blue" if self.blueTurn else "Red"
            log.debug(f"{player} player will go first")
    def calculate_pos(self,startPlace):
        return startPlace[0]*6 + startPlace[1]  
    def __str__(self):
        return self.showState()
    def showState(self):
        
        man=" " * 10
        man=man + Back.BLUE+ f"{self.board[3]:02d}"
        man+=(Style.RESET_ALL)
        man+="\n" + " "*9
        man+= Back.BLUE+ f"{self.board[4]:02d} {self.board[2]:02d}"
        man+=(Style.RESET_ALL)
        man+="\n" + " "*9
        man+=(Style.RESET_ALL)
        man+= Back.BLUE+ f"{self.board[5]:02d} {self.board[1]:02d}"
        man+=(Style.RESET_ALL) + "\n"
        man+= Back.RED+ f"{self.board[9]:02d} {self.board[8]:02d} {self.board[7]:02d} {self.board[6]:02d}"
        man+=" " 
        man+=(Style.RESET_ALL)
        man+=Back.BLUE + f"{self.board[0]:02d}"
        man+=(Style.RESET_ALL)
        man+=Back.RED
        man+=" "
        man+=f"{self.board[23]:02d} {self.board[22]:02d}"
        man+=(Style.RESET_ALL) +  "\n"
        man+=" " * 3
        man+=Back.RED
        man+=f"{self.board[10]:02d} {self.board[11]:02d} "
        man+=Back.BLUE + f"{self.board[12]:02d} "
        man+=Back.RED + f"{self.board[18]:02d} {self.board[19]:02d} {self.board[20]:02d} {self.board[21]:02d}"
        man+=(Style.RESET_ALL) + "\n"
        man+=" " * 9
        man+=Back.BLUE+ f"{self.board[13]:02d} {self.board[17]:02d}"
        man+=(Style.RESET_ALL) + "\n"
        man+=" " * 9
        man+=Back.BLUE+ f"{self.board[14]:02d} {self.board[16]:02d}"
        man+=(Style.RESET_ALL) + "\n"
        man+=" "*10
        man+=(Style.RESET_ALL)
        man+=Back.BLUE+f"{self.board[15]:02d}" +(Style.RESET_ALL) + (Style.RESET_ALL)
        return man
    def processPMove(self,action):
        self.placeStones(action.position,action.clockwise,action.skip)

     # function that places stone ,bool for clockwise ,  boolean to skip over oppnets mancal check it you go over the board 
     # args: startplace tuple(boardindex,specific marble location)
    def placeStones(self,startPlace,clockwise,skip):
        bluePlayer=True if startPlace[0] in Model.BLUE_P else False
        
        # calculate where we start 
        startPlaceIndex=self.calculate_pos(startPlace)

        # get the number of stones we need to distributate
        numStones=self.board[startPlaceIndex]

        # setting the place we start to zero
        self.board[startPlaceIndex]=0

        # if it's clockwise then we go starting spot 
        step= 1 if clockwise else -1
        MAN_I=[3,9,15,21]
        currentIndex=startPlaceIndex
        # we first move where we are about to place the stone 
        LAST_ELE=23
        FIR_ELE=0
        while numStones !=0:
            # check for special conditions whether we are at the end or begginign of the list
            if currentIndex == LAST_ELE:
                currentIndex= 0 if step > 0 else LAST_ELE-1

            elif currentIndex ==0 :
                currentIndex= LAST_ELE if step < 0 else 1

            else:
                currentIndex+=step

            
            # means we're not skipping mancalas 
            op_man=Model.RED_P if bluePlayer else Model.BLUE_P
            op_man=[x*6 +3 for x in op_man]
            # if we've reached an opponent mancala
            if currentIndex in op_man:
                if  skip:
                        continue
                    
                else:
                    self.board[currentIndex]+=1
                    numStones-=1
                    self.processSteal(bluePlayer,currentIndex)

            else:
                self.board[currentIndex]+=1
                numStones-=1

        self.processSteal(bluePlayer,currentIndex)        
        self.processLastMove(bluePlayer,currentIndex)   
        self.blueTurn=self.turnCheck(bluePlayer,currentIndex)
        

    def processSteal(self,playerBlue,currentIndex):
        #first figure out who the player is 

        # If it's a mancala piecea and it's not the own player mancal
        if playerBlue and currentIndex  in [x*6 +3 for x in Model.RED_P]:
            # means blue player is in an opponent mancalas
            if self.board[currentIndex] >=2:
                blue_mancala=Model.BLUE_P[0] *6 +3
                self.board[currentIndex]-=2
                self.board[blue_mancala]+=2

        elif not playerBlue and currentIndex in [x*6 +3 for x in Model.BLUE_P]:
            if self.board[currentIndex] >=2:
                blue_mancala=Model.RED_P[0] *6 +3
                self.board[currentIndex]-=2
                self.board[blue_mancala]+=2

       
            


    
    def processLastMove(self,bluePlayer,index):
        # check to see if it has one rock
        if self.board[index]==1 and index in [0,6,12,18]:
            targetMancala=Model.BLUE_P[0] +3 if bluePlayer else Model.RED_P[0] *6 +3 
            self.board[index]=0
            self.board[targetMancala]+=1

            blue_t=[0,12]
            red_t=[6,18]
            targets= red_t if index in blue_t else blue_t
            for x in targets:
                self.board[targetMancala]+=self.board[x]
                self.board[x]=0
        

            
            
    def isValidMove(self,coordinate):
        return False if self.board[self.calculate_pos(coordinate)] == 0 else True


    def turnCheck(self,bluePlayer,index):
        if bluePlayer:
            bluePlayerM=[3,15]
            if index in bluePlayerM:
                return True

            else :
                return False 

        else:
            redPlayerM=[9,21]
            if index in redPlayerM:
                return False
            else:
                return True
    def gameOver(self):
        # check blue player slots
        MAN_I=[3,9,15,21]
        num_blues_stones=0
        blue_p_startIndexs=[0,2]
        for startIndex in blue_p_startIndexs:
            firstElement=startIndex*6 
            for otherIndex in range(6):
                currentIndex=firstElement+otherIndex
                stones_index=self.board[currentIndex] if currentIndex not in MAN_I else 0
                num_blues_stones+=stones_index

        red_stones=0
        red_p_startIndexs=[1,3]
        for startIndex in red_p_startIndexs:
            firstElement=startIndex*6 
            for otherIndex in range(6):
                currentIndex=firstElement+otherIndex
                stones_index=self.board[currentIndex] if currentIndex not in MAN_I else 0
                red_stones+=stones_index
        return red_stones ==0 or num_blues_stones== 0  
    def playerScores(self):
            # check blue player slots
        num_blues_stones=0
        blue_p_startIndexs=[0,2]
        for startIndex in blue_p_startIndexs:
            firstElement=startIndex*6 
            for otherIndex in range(6):
                currentIndex=firstElement+otherIndex
                stones_index=self.board[currentIndex] 
                num_blues_stones+=stones_index

        red_stones=0
        red_p_startIndexs=[1,3] 
        for startIndex in red_p_startIndexs:
            firstElement=startIndex*6 
            for otherIndex in range(6):
                currentIndex=firstElement+otherIndex
                stones_index=self.board[currentIndex] 
                red_stones+=stones_index
        results=f"Red Player {red_stones}\n Blue Player {num_blues_stones}"
        print(results)

class Player:
    def __init__(self,isBluePlayer):
        self.nCount=0
        self.bluePlayer=isBluePlayer
        self.boardI=Model.BLUE_P if self.bluePlayer else Model.RED_P

    def possibleMoves(self):
        moves=list()
        for boardPos in self.boardI:
            for y in range(6):
                for some in [True,False]:
                    for skip in [True,False]:
                        if y != 3:
                            action=Action((boardPos,y),some,skip)
                            moves.append(action)
        return moves

    def oppMoves(self):
        moves=list()
        boardI=Model.RED_P if self.bluePlayer else Model.BLUE_P
        for boardPos in boardI:
            for y in range(6):
                for some in [True,False]:
                    for skip in [True,False]:
                        if y != 3:
                            action=Action((boardPos,y),some,skip)
                            moves.append(action)

        return moves


class Human(Player):
    def __init__(self,isBluePlayer):
        super().__init__(isBluePlayer)

    def move(self,model):
        invalid=False
        while(not invalid):
            boardProp="which board do you want to make a move on ? "
            board=int(input(boardProp))
            index=int(input("Choose an index on that selected board"))
            clockwise=input("Clockwise? press y for yes , anything else for no ")
            skip=input("Do you want to skip Mancalas press y for yes , anything else for no ")
            clockwise= True if clockwise == "y" else False
            skip=True if skip == "y" else False
            startPos=(board,index)
            action=Action(startPos,clockwise,skip)
 
            invalid= action in self.possibleMoves() and model.isValidMove(startPos)

        return action



class AI(Player):
    def __init__(self,isBluePlayer,depth,heuristic):
        self.nCount=0
        self.depth=depth
        self.h=heuristic
        super().__init__(isBluePlayer)
    
        

    def heuristic(self,state):
        return self.h(self.bluePlayer,state)

    def getSuccesors(self,model,max_v):
        possibleMoves=self.possibleMoves() if max_v else self.oppMoves()
        return [action for action in possibleMoves if model.isValidMove(action.position)]

    def move(self,model):
        return self.alpha_beta_search(model)

    def alpha_beta_search(self,state):
        copyState=deepcopy(state)
        alpha=-inf
        beta=inf
        bestAction=None
        validActions=self.getSuccesors(copyState,True)
        bestMove=None
        self.nCount=0
        for action in validActions:
            self.nCount+=1
            newState=deepcopy(copyState)
            newState.processPMove(action)
            value=self.min_val(newState,3,alpha,beta)
            if value > alpha:
                alpha =value
                bestAction=action

        print(f"Visted {self.nCount} nodes")
        return bestAction

    def max_val(self,state,depth,alpha,beta):
        if depth ==0 or state.gameOver():
            return self.heuristic(state)
        value=-inf
        copyState=deepcopy(state)
        
        bestAction=None 
        validMoves=self.getSuccesors(copyState,True)

        for action in validMoves:
            self.nCount+=1
            newState=deepcopy(state)
            newState.processPMove(action)
            value=max(value,self.min_val(newState,depth-1,alpha,beta))
            if value >=beta:
                return value

            alpha=max(alpha,value)
        return value

    def min_val(self,state,depth,alpha,beta):
        if depth ==0 or state.gameOver():
            return self.heuristic(state)
        value=inf
        copyState=deepcopy(state)
        validMoves=self.getSuccesors(copyState,False)

        for action in validMoves:
            self.nCount+=1
            newState=deepcopy(state)
            newState.processPMove(action)
            value=min(value,self.max_val(newState,depth-1,alpha,beta))
            if value <= alpha:
                return value

            alpha=min(alpha,value)
        return value

def h1(bluePlayer,model):
    boardIs=Model.BLUE_P if bluePlayer else Model.RED_P
    score=0
    for boardI in boardIs:
        index=boardI *6 +3
        score+=model.board[index]

    return score




def h2(bluePlayer,model):
    boardIs=Model.BLUE_P if bluePlayer else Model.RED_P
    boardIs2=Model.BLUE_P if not bluePlayer else Model.RED_P
    
    score=0
    for boardI in boardIs:
        index=boardI *6 +3
        score+=model.board[index]

    for boardI in boardIs2:
        index=boardI *6 +3
        score-=model.board[index]

    return score



if __name__ == "__main__":
    DEPTH=5
    model=Model(6)
    bluePlayer=Human(True)
    redPlayer=AI(False,DEPTH,h2)
    move=None
    while(not model.gameOver()):
        if model.blueTurn:
            print("BLue turn")
            move=bluePlayer.move(model)
        else:
            print("Red turn")
            move=redPlayer.move(model)
        
        model.processPMove(move)
        print(model)

    model.playerScores()
    print(model)
        

        
    