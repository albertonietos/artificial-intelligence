from abc import abstractmethod, ABC

class GameState(ABC):
    """
    Abstract base class for game states for two-player games.
    """
    
    @abstractmethod
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
        pass

    @abstractmethod
    def successor(self,player,action):
        """
        Returns the successor game state after `player` executing `action`.

        Parameters
        ----------
        player : int om [0,1]
           Current player

        action : object
           Action by `player`

        Returns
        -------
        GameState object
           Successor state
        """

    @abstractmethod
    def value(self):
        """
        Returns value of state.

        By convention, player 0 is minimizing (a low score is better)
        and player 1 maximizing (a high score is better).

        Returns
        -------
        float
           Value of this state.
        """
        pass
