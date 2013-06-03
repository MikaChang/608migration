# import basic
import init_parameter
from basic import *
from snapshot_gen import *
from init_update_func import *
from concurrent_case import *
from result_one_snapshot import *
import os
os.system('cls') # on linux / os x

### build input_dict. May change to "itertools.product" in the later version
input_dict = dict()    ### very import!!!  key to reset whole simulation

###vm migration mode  --> for mika related code --> basic.py
input_dict['migration_mode'] = 'StopNCopy'
# input_dict['migration_mode'] = 'PreCopy'

input_dict['algo_version'] = 'StrictSequence'
# input_dict['algo_version'] = 'ConCurrent'
# input_dict['algo_version'] = 'RanSequence'


### vm snapshot generate by Consolidation or LoadBalancing  --> for louis related code. --> snapshot_gen.py
input_dict['migr_type'] = 'Consolidation'
# input_dict['migr_type'] = 'LoadBalancing'

input_dict['tot_host_num'] = 16
# input_dict['tot_host_num'] = 64

input_dict['src_num'] = 4
# input_dict['src_num'] = 8
# input_dict['src_num'] = 12




######## Algorithm running
G = Global_cl(input_dict)     #global data structure
E = G.E                 # event list

# generate VM and hosts, if at least one VM have not DST --> re-run snapshot_gen_func again
keep_gen = True
result = False
while keep_gen:
    # result, vm__dict, host__dict = snapshot_gen(G, input_dict['tot_host_num'], input_dict['src_num'], input_dict['migr_type'])
    result, vm__dict, host__dict = snapshot_gen(G, input_dict['tot_host_num'], input_dict['src_num'], input_dict['migr_type'])
    if result == True:
        print 'main.py: snapshot_gen\t', result
        print 'vm_size:', len(vm__dict), 'host_size', len(host__dict)
        break
    elif result == False:
        print 'main.py: snapshot_gen\t', result
    else:
        assert(0)
        
assert(result == True)
G.all_VM__dict = vm__dict
G.all_host__dict = host__dict

# initialization of vmm transmission
print '---------->> now time:', 0, 'main.py before all vm schedule initialization'
if input_dict['algo_version'] == 'StrictSequence':
    func_SS_INIT(G)
elif input_dict['algo_version'] == 'ConCurrent':
    func_Concurrent(G, initFlag = True)
else:
    assert(0)

# print '\n\n'
print 'main.py: after initialization, some event are scheduled, event_num =\t', len(E.list)
assert(len(E.list) > 0)
# continuous event based...vmm transmission
while (len(E.list) > 0):
    result, event_obj = E.upcoming_event()
    if result == True:
        G.now = event_obj.time
        print '\n\n---------->> now time:', G.now, 'main.py --> activate one valid event. '
        
        vm_num = event_obj.vm_num
        G.all_VM__dict[vm_num].migration_over()

    else:
        print '---------->> main.py --> skip one obsolete event'

### add assert to ensure all vm_obj.status == 'completed'
print 'all events have finished, computing results for the snapshot'
output_dict = result_one_snap(G)

result_dict = dict()
result_dict['input'] = input_dict
result_dict['output'] = output_dict