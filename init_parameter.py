SET__set = set([1,2,3])  # set 1,2,3
GP__set = set([1,2,3])   # group 1,2,3
SLOTTIME = 1e-6

input_dict == dict()
input_dict['migration_mode'] = 'StopNCopy'
input_dict['migration_mode'] = 'PreCopy'


input_dict['algo_version'] = 'StrictSequence'   
input_dict['algo_version'] = 'ConCurrent'   
input_dict['acceptable_mini_VMM_data_rate'] = 0.1

input_dict['migr_type'] = 'Consolidation'
input_dict['migr_type'] = 'LoadBalancing'
