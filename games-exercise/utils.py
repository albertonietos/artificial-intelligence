
def count_calls(fun):
    """
    Wraps a function to count the number of calls.

    Parameters
    ----------
    fun : function

    Returns
    -------
    function
    """
    def f(*args, **kwargs):
        f.calls +=1
        return fun(*args,**kwargs)
    # Set calls to 0
    f.calls = 0
    # Make f look like fun
    f.__name__ = fun.__name__
    return f

