class Parameters:
    """ This class defines all parameters which are used in the pond control project.

    Methods
    ---------
    None
    """
    def __init__(self):
        """ Constructor of the Parameters class.
        """
        pass

    # database file
    DB_FILE = './teich.db'

    # system state file
    SYSTEM_STATE_FILE = './system_state.txt'

    # wait time for one refilling iteration in seconds
    FILL_TIME = 60

    # time until water level sensor is checked again in seconds
    POLLING_PERIOD_WATER_SENSOR = 120

    # time until system state is checked again if an error occurred in seconds
    SYSTEM_CHECK_TIME = 2

    # number of filling iterations until the system raises an error
    ERROR_COUNTER = 10