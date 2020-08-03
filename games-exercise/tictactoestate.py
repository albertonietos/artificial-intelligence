import gamestate

class TicTacToeState(gamestate.GameState):
    """
    The game of tic tac toe in a 3 by 3 grid grid is represented as a list 
    [ , , ,
      , , ,
      , ,  ]
    of integers in (-1,0,1). Where -1 denotes that the cell is empty, 0 denotes 
    piece placed by player 0, and denotes piece placed by player 1.

    The game representation thus assumes that the players are 0 and 1.
    """

    def __init__(self, cs = [-1]*9):
        """
        Create state with a given configuration.
        
        Parameters
        ----------
        cs : list (length 9) of int in [-1,1], optional
           The game board state. The default state is all cell values are -1,
           that is empty.
        """
        self.cells = cs
        
    def applicable_actions(self,player):
        """
        Returns a list of all applicable actions for `player` in the current 
        game state.

        Parameters
        ----------
        player : int
           Current player.

        Returns
        -------
        List of int in [0,8]
           All non-occupied locations on the game board as integer indices.
        """
        # Can ignore `player`, and only need to check which game cells are
        # empty.
        if self.value() == 0:
            return [i for i in range(0,9) if self.cells[i]==-1]
        else:
            return []

    def successor(self,player,action):
        """
        Returns the successor game state after `player` executing `action`.

        Parameters
        ----------
        player : int in [0,1]
           Current player

        action : int in [0,8]
           Game board cell where `player` places a marker.

        Returns
        -------
        GameState object
           Successor with the cell indicated by `action` occupoed by `player`.
           If the cell is already occupied (illegal move) the current state is 
           returned.
        """
        if self.cells[action] == -1:
            return TicTacToeState(self.cells[0:action] + [player] + self.cells[action+1:])
        else:
            return self

    def value(self):
        """
        Returns value of state.
        
        The values of final states are
        -1 : player 1 loses (player 0 wins)
         0 : game not finished, or draw
         1 : player 1 wins

        Returns
        -------
        float
           Value of this state as indicated above.
        """
        # rows 0
        if self.cells[0:3] == [0,0,0] or self.cells[3:6] == [0,0,0] or self.cells[6:9] == [0,0,0]:
            return -1
        # rows 1
        if self.cells[0:3] == [1,1,1] or self.cells[3:6] == [1,1,1] or self.cells[6:9] == [1,1,1]:
            return 1
        # 0 columns
        if self.cells[0]==0 and self.cells[3]==0 and self.cells[6]==0:
            return -1
        if self.cells[1]==0 and self.cells[4]==0 and self.cells[7]==0:
            return -1
        if self.cells[2]==0 and self.cells[5]==0 and self.cells[8]==0:
            return -1
        # 1 columns
        if self.cells[0]==1 and self.cells[3]==1 and self.cells[6]==1:
            return 1
        if self.cells[1]==1 and self.cells[4]==1 and self.cells[7]==1:
            return 1
        if self.cells[2]==1 and self.cells[5]==1 and self.cells[8]==1:
            return 1
        # 0 diagonals
        if self.cells[0]==0 and self.cells[4]==0 and self.cells[8]==0:
            return -1
        if self.cells[2]==0 and self.cells[4]==0 and self.cells[6]==0:
            return -1
        # 1 diagonals
        if self.cells[0]==1 and self.cells[4]==1 and self.cells[8]==1:
            return 1
        if self.cells[2]==1 and self.cells[4]==1 and self.cells[6]==1:
            return 1
        return 0


    def __str__(self):
        def row2str(l):
            s = ""
            for e in l:
                if e==-1:
                    s+="."
                else:
                    s+=str(e)
            return s
        return "\n".join([row2str(self.cells[0:3]),
                          row2str(self.cells[3:6]),
                          row2str(self.cells[6:9])])


