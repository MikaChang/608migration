import basic

def update_SetNum_GPNum_to_vm_to_host(G):
    for vm_num,vm_obj in G.all_VM__dict.items:        # categorizing all_VM into 3 Sets
        vm_set_num = vm_obj.get_set_num()
        G.SetNum_to_VM__dict[vm_set_num].add(vm_num)
        G.SetNum_to_host__dict[vm_set_num].add(vm_obj.SRCnum)
        G.SetNum_to_host__dict[vm_set_num].add(vm_obj.DSTnum)
        G.all_host__dict[vm_obj.SRCnum].waiting_vm__set.add(vm_num)
        G.all_host__dict[vm_obj.DSTnum].waiting_vm__set.add(vm_num)
        if vm_set_num==1:
            G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[1].add(vm_obj)
            G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[1].add(vm_obj)
        else:
            G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[2].add(vm_obj)
            G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[2].add(vm_obj) 
        G.SRC_host__set.add(vm_obj.SRCnum)
        G.DST_host__set.add(vm_obj.DSTnum)

    G.GPNum_to_VM__dict[1] = G.SetNum_to_VM__dict[1]  # categorizing GPs by 3 Sets
    G.GPNum_to_VM__dict[2] = G.SetNum_to_VM__dict[2] | G.SetNum_to_VM__dict[3]
    G.GPNum_to_host__dict[1] = G.SetNum_to_host__dict[1]
    G.GPNum_to_host__dict[2] = G.SetNum_to_host__dict[2] | G.SetNum_to_host__dict[3] - G.SetNum_to_host__dict[1]



def func_SS_INIT(G):
    ### Need assignment, ex vmm bw, host bw ...
    ### Need calculate SB ratio

    update_SetNum_GPNum_to_vm_to_host(G)
    
    DST_GP1 = G.DST_host__set & GPNum_to_host__dict[1]   # find those destination host in Group 1
    for host_num in DST_GP1:
        host_obj = G.all_host__dict[host_num]
        seq_vm_obj__list = sorted(host_obj.GPNum_to_VM__dict[1], key=lambda VM_cl2: VM_cl2.dnSBratio )
        
        for vm_obj in seq_vm_obj__list:
            result, miniRate = vm_obj.speed_checking(BW_mode = 'full', domi_node = 'DST')
            if result == 'success':
                vm_obj.assign_VM_BW(miniRate)
                break
            else:
                SRCnum = vm_obj.SRCnum
                G.all_host__dict[SRCnum].reg_q__Set.add(vm_obj.vm_num)
                break


    SRC_GP2 = G.SRC_host__set & GPNum_to_host__dict[2]    #find those source host in Group 2
    for host_num in SRC_GP2:
        host_obj = G.all_host__dict[host_num]
        ### mika
        seq_vm_obj__list = sorted(host_obj.GPNum_to_VM__dict[2], key=lambda VM_cl2: VM_cl2.upBSratio )
        
        for vm_obj in seq_vm_obj__list:
            result, miniRate = vm_obj.speed_checking(BW_mode = 'full', domi_node = 'SRC')
            if result == 'success':
                vm_obj.assign_VM_BW(miniRate)
                break
            else:
                DSTnum = vm_obj.DSTnum
                G.all_host__dict[DSTnum].reg_q__Set.add(vm_obj.vm_num)
                break


def func_SS_update_ongoing(G,finish_vm):
    SRC_num = G.all_VM__dict[finish_vm].SRCnum
    DST_num = G.all_VM__dict[finish_vm].DSTnum
    SRC_host = G.all_host__dict[SRC_num]
    DST_host = G.all_host__dict[DST_num]
    fin_vm_set_num = G.all_VM__dict[finish_vm].set_num

    if fin_vm_set_num==1:
        SRCobj.GPNum_to_VM__dict[1] -= set([finish_vm])
        DSTobj.GPNum_to_VM__dict[1] -= set([finish_vm])
    else :
        SRCobj.GPNum_to_VM__dict[2] -= set([finish_vm])
        DSTobj.GPNum_to_VM__dict[2] -= set([finish_vm])

    G.SetNum_to_VM__dict[fin_vm_set_num] -= set([finish_vm])
    G.SetNum_to_host__dict[fin_vm_set_num] -= set([SRC_num])
    G.SetNum_to_host__dict[fin_vm_set_num] -= set([DST_num])

    for vm_num in SRC_host.waiting_vm__set:
        vm_obj = G.all_VM__dict[vm_num]
        prev_vm_set_num = vm_obj.set_num
        now_vm_set_num = vm_obj.get_set_num()          #recalculate to catgorize sets
        if prev_vm_set_num != now_vm_set_num:
            G.SetNum_to_VM__dict[prev_vm_set_num] -= set([vm_num])
            G.SetNum_to_host__dict[prev_vm_set_num] -= set([vm_num])
            G.SetNum_to_host__dict[prev_vm_set_num] -= set([vm_num])
            if prev_vm_set_num==1:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[1] -= set([vm_num])
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[1] -= set([vm_num])
            else:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[2] -= set([vm_num])
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[2] -= set([vm_num])

            G.SetNum_to_VM__dict[now_vm_set_num].add(vm_num)
            G.SetNum_to_host__dict[now_vm_set_num].add(vm_obj.SRCnum)
            G.SetNum_to_host__dict[now_vm_set_num].add(vm_obj.DSTnum)
            if now_vm_set_num==1:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[1].add(vm_obj)
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[1].add(vm_obj)
            else:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[2].add(vm_obj)
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[2].add(vm_obj) 

    for vm_num in DST_host.waiting_vm__set:
        vm_obj = G.all_VM__dict[vm_num]
        prev_vm_set_num = vm_obj.set_num
        now_vm_set_num = vm_obj.get_set_num()          #recalculate to catgorize sets
        if prev_vm_set_num != now_vm_set_num:
            G.SetNum_to_VM__dict[prev_vm_set_num] -= set([vm_num])
            G.SetNum_to_host__dict[prev_vm_set_num] -= set([vm_num])
            G.SetNum_to_host__dict[prev_vm_set_num] -= set([vm_num])
            if prev_vm_set_num==1:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[1] -= set([vm_num])
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[1] -= set([vm_num])
            else:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[2] -= set([vm_num])
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[2] -= set([vm_num])

            G.SetNum_to_VM__dict[now_vm_set_num].add(vm_num)
            G.SetNum_to_host__dict[now_vm_set_num].add(vm_obj.SRCnum)
            G.SetNum_to_host__dict[now_vm_set_num].add(vm_obj.DSTnum)
            if now_vm_set_num==1:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[1].add(vm_obj)
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[1].add(vm_obj)
            else:
                G.all_host__dict[vm_obj.SRCnum].GPNum_to_VM__dict[2].add(vm_obj)
                G.all_host__dict[vm_obj.DSTnum].GPNum_to_VM__dict[2].add(vm_obj) 
    
    G.GPNum_to_VM__dict[1] = G.SetNum_to_VM__dict[1]  # categorizing GPs by 3 Sets
    G.GPNum_to_VM__dict[2] = G.SetNum_to_VM__dict[2] | G.SetNum_to_VM__dict[3]
    G.GPNum_to_host__dict[1] = G.SetNum_to_host__dict[1]
    G.GPNum_to_host__dict[2] = G.SetNum_to_host__dict[2] | G.SetNum_to_host__dict[3] - G.SetNum_to_host__dict[1]
