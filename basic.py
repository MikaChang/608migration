### wahahaha.....test for GitHub

from __future__ import division
import math

SET__set = set([1,2,3])  # set 1,2,3
GP__set = set([1,2,3])   # group 1,2,3

import function_Louis_130529 as func
import init_func_mika_130529_2 as init_func

acceptable_mini_VMM_data_rate = 0.1

SLOTTIME = 1e-6

class Global_cl():
    def __init__(self):    
        self.E =  Event_list_cl()  # declare event_list, we store event_obj inside
        
        self.migration_mode = 'StopNCopy'      # 'PreCopy' or 'StopNCopy'
        
        self.now = 0            # record  'NOW' time    
        
        self.all_host__dict = dict()    # store all the host_obj   e.g.  all_host__dict[host_num] = host_obj
        self.all_VM__dict = dict()    # store all the VM_obj   e.g.  all_VM__dict[vm_num] = vm_obj
        
        self.SRC_host__set = set() # store all the SRC host_num  e.g. (host_num, host_num)
        self.DST_host__set = set()  # store all the DST host_num
        
        self.SetNum_to_VM__dict = dict()   # key: set number   value: vm_num set
        for i in SET__set:
            self.SetNum_to_VM__dict[i] = set()
                      
        self.SetNum_to_host__dict = dict()   # key: set number   value: host_num set
        for i in SET__set:
            self.SetNum_to_host__dict[i] = set()        
            
        self.GPNum_to_VM__dict = dict()  # key: group number   value: VM_num set
        for i in GP__set:
            self.GPNum_to_VM__dict[i] = set()
            
        self.GPNum_to_host__dict = dict()  # key: group number   value: host_num set
        for i in GP__set:
            self.GPNum_to_host__dict[i] = set()



class Event_list_cl():
    def __init__(self,G):
        self.list = []
        self.G = G
        
    def upcoming_event(self):
        # if len(list) == 0:
            # return False, None           

        tmpL = sorted(self.list, key=lambda Event_cl: Event_cl.time)
        event_obj = tmpL.pop(0)
        if event_obj.time != all_VM__dict[event_obj.vm_num].last_migration_event_finish_time
            return False, None

        return True, event_obj
        
    def insert(self, event_obj):
        self.list.append(event_obj)
        


class Host_cl():
    def __init__(self, G, type, host_num):
        self.G = G
        self.type = type   # type --> 'SRC' or 'DST'
        ### Louis
        self.size = 100.0
        self.BWC = 100.0
        self.upBW = 0.0
        self.dnBW = 0.0
        self.sigmaC = 100.0
        self.sigma = 0.0
        self.host_num = host_num
        ### Louis
        self.upRBW = 0.0   # now residual up BW
        self.dnRBW = 0.0   # now residual down BW
        self.Initial_upRBW = 0.0   # Initial residual up BW after all VMM complete
        self.Initial_dnRBW = 0.0   # Initial residual down BW after all VMM complete
        self.Final_upRBW = 0.0   # Final residual up BW after all VMM complete
        self.Final_dnRBW = 0.0   # Final residual down BW after all VMM complete
        
        
        # self.all_VM__dict = dict()  #dict to record VM inside the host
        
        self.waiting_vm__set = set()  # set() to record the  vm_num (waiting migration)
        self.sending_vm__set = set()  # set() to record the  vm_num (sending migration)
        
        self.reg_q__Set = set()   # set() to record the vm_num waiting for migrations with registration
        
        for i in GP__set:
            self.GPNum_to_VM__dict[i] = set()   # key: group number   value: VM_obj set



        
class VM_cl2():
    def __init__(self, G, ori_size, vm_num, upSBW, dnSBW, sigma, SRCnum):
        self.G = G
        self.ori_size = float(ori_size) # original size of VM
        ### Louis
        self.sigma = float(sigma) 
        ### Louis
        self.remain_size = float(ori_size)  # after some time period, the remaining size for migration
        self.upSBW = float(upSBW)  #vm uplink service BW
        self.dnSBW = float(dnSBW)  #vm downlink service BW
        
        self.upBSratio = float(upSBW) / ori_size
        self.upSBratio = ori_size / float(upSBW)
        self.dnBSratio = float(dnSBW) / ori_size
        self.dnSBratio = ori_size/(float(dnSBW))
        
        self.latest_data_rate
        
        # self.host_num = host_num  #vm belong to # host (now position)
        self.vm_num = vm_num  #vm number
        
        self.SRCnum = SRCnum  #the host SRC number
        self.DSTnum = None  #the host DST number
        self.status = "waiting"     # status ==> 'waiting', 'sending', 'completed'
        # self.dominant = "Null"   # dominant host = 'SRC' or 'DST'    ###useless
        self.set_type = 'Null'   # 1 or 2 or 3  ==> use number not string!!!!!
        self.set_num = None  # value = 1,2,3
        
        self.migration_start_time = 0
        self.migration_over_time = 0
        self.last_migration_event_finish_time = 0  # 1) let event queue check whether the event from event queue is the latest or the expired event. 2) let node update his migration progress upon event. VM can compute the period during two time checkpoint, thus the migration progress can be computed
        
        
        
        
        
    def next_status(self):
        if self.status == 'waiting':
            self.status = 'sending'
        elif self.status == 'sending':
            self.status = 'completed'
        else:
            assert(0)
        
    def get_set_num(self):     # return the set number for each VMM, e.g. 1 2 3   <== int. only
        SRChost = all_host__dict[self.SRCnum]
        DSThost = all_host__dict[self.DSTnum]
        
        SRC_now = SRChost.upRBW
        if self.migration_mode == 'StopNCopy':
            SRC_now += self.upSBW
        SRC_end = SRChost.Final_upRBW
        DST_now = DSThost.dnRBW
        DST_end = DSThost.Final_dnRBW
        
        if SRC_now >= DST_now and SRC_end >= DST_end:
            self.set_num = 1
        elif SRC_now < DST_now and SRC_end >= DST_end:
            self.set_num = 2
        elif SRC_now < DST_now and SRC_end < DST_end:
            self.set_num = 3
        else:
            assert(0)
        
        return self.set_num

            


    def adjust_VM_BW(self, rate):  ## still working !!!
        assert(self.status == 'sending')
        SRCobj = G.all_host__dict[self.SRCnum]
        DSTobj = G.all_host__dict[self.DSTnum]
        
        #release old data rate for SRC and DST
        SRCobj.upRBW += self.latest_data_rate
        DSTobj.dnRBW += self.latest_data_rate
        SRCobj.upRBW -= rate
        DSTobj.dnRBW -= rate

        assert(SRCobj.upRBW >= 0)
        assert(DSTobj.dnRBW >= 0)                
        self.latest_data_rate = rate
        
        # update  vm_obj.remain_size according latest_data_rate
        
        
        ### schedule Event_cl() into event list
        finish_time = self.compute_finish_time()
        event_obj = Event_cl(type = 'vm finish', finish_time, self.vm_num, info__dict = dict() )
        
        assert (self.migration_start_time != 0)
        self.last_migration_event_finish_time = finish_time
        self.G.E.list.insert(event_obj)
        

    def release_BW(self):   # release the BW usage.   SRC release uplink, DST release dnlink
        SRCobj = G.all_host__dict[self.SRCnum]
        DSTobj = G.all_host__dict[self.DSTnum]
        SRCobj.upRBW += self.latest_data_rate
        DSTobj.dnRBW += self.latest_data_rate
        DSTobj.upRBW -= self.upSBW
        DSTobj.dnRBW -= self.dnSBW
        if self.migration_mode == 'PreCopy':
            SRCobj.upRBW += self.upSBW    # PreCopy mode!!!
            SRCobj.dnRBW += self.dnSBW    # PreCopy mode!!!
        else:
            assert (self.migration_mode == 'StopNCopy')
        assert(SRCobj.upRBW >= 0)
        assert(DSTobj.dnRBW >= 0)        
        
        SRCobj.sending_vm__set -= set([self.vm_num])
        DSTobj.sending_vm__set -= set([self.vm_num])        
        
        ###update vm_obj.status
        self.next_status()

        self.migration_over_time = self.G.now


    
    def migration_over(self):
        self.release_BW(self)
        init_func.func_SS_update_ongoing(G,self.vm_num)
        ### can change to multiple SS G functions
        func.func_SS(self.G, 1, 'random')
        func.func_SS(self.G, 2, 'random')
        
        
        
    def assign_VM_BW(self, rate):
        assert(self.status == 'waiting')
    
        ### assign VM BW into SRC, DST
        SRCobj = G.all_host__dict[self.SRCnum]
        DSTobj = G.all_host__dict[self.DSTnum]
        if self.migration_mode == 'StopNCopy':
            SRCobj.upRBW += self.upSBW    # StopNCopy mode!!!
            SRCobj.dnRBW += self.dnSBW    # StopNCopy mode!!!
        else:
            assert (self.migration_mode == 'PreCopy')
        SRCobj.upRBW -= rate
        assert(SRCobj.upRBW >= 0)
        DSTobj.dnRBW -= rate
        assert(DSTobj.dnRBW >= 0)
        
        self.next_status()
        self.latest_data_rate = rate
        SRCobj.waiting_vm__set -= set([self.vm_num])
        DSTobj.waiting_vm__set -= set([self.vm_num])
        SRCobj.sending_vm__set += set([self.vm_num])
        DSTobj.sending_vm__set += set([self.vm_num])
        
        ### schedule Event_cl() into event list
        finish_time = self.compute_finish_time()
        event_obj = Event_cl(type = 'vm finish', finish_time, self.vm_num, info__dict = dict() )
        
        if self.migration_start_time == 0:
            self.migration_start_time = self.G.now
        self.last_migration_event_finish_time = finish_time
        self.G.E.list.insert(event_obj)

        
    def compute_finish_time(self):
        time = self.remain_size / float(self.latest_data_rate)
        finish_time = int(math.ceil(time / SLOTTIME))
        finish_time *= SLOTTIME
        finish_time += G.now 
        return finish_time
        
    def speed_checking(self, BW_mode, domi_node):    # e.g. BW_mode = 'full', 'partial'   domi_node = 'SRC', 'DST'
        SRCobj = G.all_host__dict[self.SRCnum]
        DSTobj = G.all_host__dict[self.DSTnum]
        upRate = SRCobj.upRBW
        if self.migration_mode == 'StopNCopy':
            upRate += self.upSBW   # StopNCopy mode!!!
        dnRate = DSTobj.dnRBW
        minRate = min(upRate, dnRate)
        
        if minRate == 0 or minRate <= acceptable_mini_VMM_data_rate:
            return 'fail', 0
        
        if BW_mode == 'full':
            if domi_node =='DST':
                assert (minRate == dnRate)
                mode_result = 'success'
            elif domi_node =='SRC':
                assert (minRate == upRate)
                mode_result = 'success'
            else:
                assert(0)
        else:
            assert(0)

        return 'success', minRate        
        

    
    
    
    
        

class Event_cl():
    def __init__(self, G, type = 'vm finish', time, vm_num, info__dict = dict() ):
        self.G = G
        self.type = type
        self.time = time
        self.vm_num = vm_num
        self.info__dict = info__dict
        
        
