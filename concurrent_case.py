import basic

def func_Concurrent(G):
    ### Need assignment, ex vmm bw, host bw ...
    ### Need calculate SB ratio
    totalVM = 0
    readyVM = 0
    ### need modification
    bwStep = linkBW*0.001
    ###

    for vm_num,vm_obj in G.all_VM__dict.items:
        if vm_obj.status == waiting || vm_obj.status == sending:
            vm_obj.latest_data_rate = 0
            totalVM+=1

    while readyVM < totalVM:
        for vm_num,vm_obj in G.all_VM__dict.items:
            if vm_obj.status == waiting || vm_obj.status == sending:

                SRCobj = G.all_host__dict[self.SRCnum]
                DSTobj = G.all_host__dict[self.DSTnum]
                if SRCobj.upRBW >= bwStep && DSTobj.dnRBW >= bwStep:
                    vm_obj.latest_data_rate += bwStep
                    SRCobj.upRBW -= bwStep
                    DSTobj.dnRBW -= bwStep
                else :
                    vm_obj.latest_data_rate += min(SRCobj.upRBW,DSTobj.dnRBW)
                    SRCobj.upRBW -= min(SRCobj.upRBW,DSTobj.dnRBW)
                    DSTobj.dnRBW -= min(SRCobj.upRBW,DSTobj.dnRBW)
                    readyVM +=1

    for vm_num,vm_obj in G.all_VM__dict.items:
        if vm_obj.status == waiting || vm_obj.status == sending:
            time = vm_obj.compute_finish_time()
            event_obj = Event_cl(type = 'vm finish', time, vm_num, info__dict = dict() )
            self.G.E.list.insert(event_obj)

        ## what's this
        ##if self.migration_start_time == 0:
        ##    self.migration_start_time = self.G.now
        ##self.last_migration_event_time = self.G.now
        ##self.G.E.list.insert(event_obj)






