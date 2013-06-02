from __future__ import division
import math

# for StrictSequence algo
import function as func

# for ConCurrent
import concurrent_case as ConCur_py


import init_update_func as init_func


# for snapshot generation
import snapshot_gen as snapshot_gen_func

####
SET__set = set([1,2,3])  # set 1,2,3
GP__set = set([1,2,3])   # group 1,2,3
SLOTTIME = 1e-6

ACCEPTABLE_MINI_VMM_DATA_RATE = 0.1