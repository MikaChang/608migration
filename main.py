import basic


G = Global_cl()     #global data structure
E = G.E                 # event list

init_func.func_SS_INIT(G)

while (len(E.list) > 0):
    result, event_obj = E.upcoming_event()
    if result == True:
        G.now = event_obj.time
        vm_num = event_obj.vm_num
        all_VM__dict[vm_num].migration_over()

### add assert to ensure all vm_obj.status == 'completed'

print 'all events have finished'