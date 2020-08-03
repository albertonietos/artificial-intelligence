import gamestate

class PursuitState(gamestate.GameState):
    """
    Describes a 'police-and-robbers-game' where player 0 is trying to catch 
    (enter the same location as) player 1, who in turn is trying to collect 
    reward at game locations without being caught.
    
    The game board is a grid of integers, where -1 denotes a wall (cell that
    cannot be entered) or some value, n, which is the reward to player 1 when
    entering the lication.
    
    If player 0 enters the same location as player 1, there is a large negative 
    value (-1000) to the game value (thus benefiting player 0 whi is minimizing).

    """
    # Class attributes.
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    ACTIONS = [NORTH,SOUTH,WEST,EAST]

    def __init__(self,x_max,y_max,cells,x0,y0,x1,y1,reward):
        """
        Create a PursuitState.

        Parameters
        ----------
        x_max : int > 0
           Number of grid columns.
        y_max : int > 0
           Number of grid rows.
        cells : list of list of int
           Grid, where a negative value indicates that a cell can not be 
           entered, and any other value is a reward for player 1.
        x0 : int in [0,x_max[
           Player 0 x-coordinate.
        y0 : int in [0,y_max[
           Player 0 y-coordnate.
        x1 : int in [0,x_max[
           Player 1 x-coordinate.
        y1 : int in [0,y_max[
           Player 1 y-coordnate.
        reward : int
           Current value of the game.
        """
        self.x_max = x_max
        self.y_max = y_max
        self.grid = cells
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.reward = reward

    def possible(self,player,action):
        """
        Check if `action` by `player` is a possible move.
        
        Helper method.
        
        Parameters
        ----------
        player : int in [0,1]
        action : int in PursuitState.ACTIONS
        
        Returns
        -------
        bool
           True if action is possible in this state.
        """
        if player==0:
            x=self.x0
            y=self.y0
        else:
            x=self.x1
            y=self.y1
        if action==self.NORTH and y==0:
            return False
        if action==self.SOUTH and y==self.y_max:
            return False
        if action==self.WEST and x==0:
            return False
        if action==self.EAST and x==self.x_max:
            return False
        if action==self.NORTH:
            y -= 1
        if action==self.SOUTH:
            y += 1
        if action==self.WEST:
            x -= 1
        if action==self.EAST:
            x += 1
        if self.grid[y][x] == -1:
            return False
        return True

    def applicable_actions(self,player):
        """
        Returns a list of all applicable actions for `player` in the current 
        game state.

        Parameters
        ----------
        player : int in [0,1]
           Current player.

        Returns
        -------
        List of objects
           Applicable actions.

        """
        return [x for x in self.ACTIONS if self.possible(player,x)]

    def successor(self,player,action):
        """
        Returns the successor game state after `player` executing `action`.

        Parameters
        ----------
        player : int om [0,1]
           Current player

        action : int in PursuitState.ACTIONS
           Action by `player`

        Returns
        -------
        PursuitState object
           Successor state
        """
        if player==0:
            x=self.x0
            y=self.y0
        else:
            x=self.x1
            y=self.y1
        if action==self.NORTH and y==0:
            return self
        if action==self.SOUTH and y==self.y_max:
            return self
        if action==self.WEST and x==0:
            return self
        if action==self.EAST and x==self.x_max:
            return self
        if action==self.NORTH:
            y -= 1
        if action==self.SOUTH:
            y += 1
        if action==self.WEST:
            x -= 1
        if action==self.EAST:
            x += 1
        if self.grid[y][x] == -1:
            return self
        newreward = self.reward
        if player==0:
            if(x==self.x1 and y==self.y1):
                newreward -= 1000
            return PursuitState(self.x_max,self.y_max,self.grid,x,y,self.x1,self.y1,newreward)
        else:
            if(self.x0==x and self.y0==y):
                newreward -= 1000
            newreward += self.grid[y][x]
        return PursuitState(self.x_max,self.y_max,self.grid,self.x0,self.y0,x,y,newreward)

    def value(self):
        """
        Returns value of state (state reward).

        By convention, player 0 is minimizing (a low score is better)
        and player 1 maximizing (a high score is better).

        Returns
        -------
        float
           Value of this state.
        """
        return self.reward

    def __str__(self):
        ss = []
        for y in range(0,self.y_max+1):
            s = ""
            for x in range(0,self.x_max+1):
                if self.x0==x and self.y0==y and self.x1==x and self.y1==y:
                    s +="X"
                elif self.x0==x and self.y0==y:
                    s+="P"
                elif self.x1==x and self.y1==y:
                    s+="C"
                elif self.grid[y][x] == -1:
                    s+="#"
                else:
                    s+=str(self.grid[y][x])
            ss.append(s)
        return "\n".join(ss)

    # def __copy__(self):
    #     return PursuitState(self.x_max, self.y_max, 
