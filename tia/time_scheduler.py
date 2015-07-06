"""
Management of the time and pauses.

This is needed because the real time engine is based on the time,
and pauses activation breaf the linearity of the time.

This module provides a time access, considering and encapsuling
the delay induced by pauses.

"""
import time as stdtime


###############################################################################
# DECLARATIONS
###############################################################################
# at the beginning the lateness of time induced by pauses is zero
late_time  = 0.0
pause_time = None


###############################################################################
# TIME ACCESS
###############################################################################
def time():
    return pause_time if pause_time else (stdtime.time() - late_time)

def sleep(x):
    return stdtime.sleep(x)



###############################################################################
# PAUSE MANAGEMENT
###############################################################################
def is_pause():
    'True if time is paused'
    global pause_time
    return pause_time is not None

def pause():
    'turn on the pause'
    global pause_time
    pause_time = stdtime.time()

def unpause():
    'turn off the pause'
    global late_time, pause_time
    if pause_time is None: return
    # add to late time the amount of time that pass since the pause activation
    late_time += stdtime.time() - pause_time
    pause_time = None

