import basic

def func_ran_disjoint_init(G):
    print 'func_ran_disjoint_init, randomCase.py'
    #disjoint_VM__set
    #non_disjoint__set
    #waiting__set
    disjoint_host__set = set()
    
    for vm_num, vm_obj in G.all_VM__dict.items():
        if vm_obj.SRCnum not in disjoint_host__set and vm_obj.DSTnum not in disjoint_host__set:
            G.disjoint_VM__set.add(vm_num)
            disjoint_host__set.add(vm_obj.SRCnum)
            disjoint_host__set.add(vm_obj.DSTnum)
    
    for vm_num in disjoint_VM__set:
        vm_obj = G.all_VM__dict[vm_num]
        if vm_obj.migration_mode == 'StopNCopy':
            minRate = min(G.all_host__dict[vm_obj.SRCnum].upRBW + vm_obj.upSBW,
                                    G.all_host__dict[vm_obj.DSTnum].dnRBW)
        else:
            minRate = min(G.all_host__dict[vm_obj.SRCnum].upRBW,G.all_host__dict[vm_obj.DSTnum].dnRBW)
        vm_obj.assign_VM_BW(minRate)
    
    tmp_set = set()
    tmp_set = G.all_VM__dict.keys()
    tmp_set = tmp_set - G.disjoint_VM__set
    
    for vm_num in tmp_set:
        vm_obj = G.all_VM__dict[vm_num]
        result, dataRate = vm_obj.speed_checking('partial',None)
        if result == 'fail':
            continue
        else:
            vm_obj.assign_VM_BW(dataRate)
            G.non_disjoint__set.add(vm_num)
            
    G.waiting__set = G.all_VM__dict.keys()
    G.waiting__set = G.waiting__set - G.disjoint_VM__set - G.non_disjoint__set
        