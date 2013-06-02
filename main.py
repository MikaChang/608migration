# import basic
import init_parameter


#### build input_dict
input_dict == dict()    ### very import!!!  key to reset whole simulation
#vm migration mode  --> for mika related code
input_dict['migration_mode'] = 'StopNCopy'
input_dict['migration_mode'] = 'PreCopy'

input_dict['algo_version'] = 'StrictSequence'
input_dict['algo_version'] = 'ConCurrent'


# vm snapshot generate by Consolidation or LoadBalancing  --> for louis related code. --> snapshot_gen.py
input_dict['migr_type'] = 'Consolidation'
input_dict['migr_type'] = 'LoadBalancing'

input_dict['tot_host_num'] = 16
input_dict['tot_host_num'] = 64

input_dict['src_num'] = 4
input_dict['src_num'] = 8
input_dict['src_num'] = 12




######## Algorithm running
G = Global_cl()     #global data structure
E = G.E                 # event list

# generate VM and hosts
snapshot_gen_func.

if input_dict['algo_version'] == 'StrictSequence':
    init_func.func_SS_INIT(G)
elif input_dict['algo_version'] == 'ConCurrent':
    

while (len(E.list) > 0):
    result, event_obj = E.upcoming_event()
    if result == True:
        G.now = event_obj.time
        vm_num = event_obj.vm_num
        all_VM__dict[vm_num].migration_over()

### add assert to ensure all vm_obj.status == 'completed'

print 'all events have finished'
######## StrictSequence algo.