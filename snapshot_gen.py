import math
import random

def snapshot_gen(tot_host_num, src_num, migr_type):
    ### tot_host_num can be 16 or 64
    ### src_num can be [4, 8, 12] in 16_mode
    ### migr_type can be 'Consolidation' or 'LoadBalancing'
    
    