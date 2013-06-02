import init_parameter
from init_parameter import SET__set, GP__set, SLOTTIME, ACCEPTABLE_MINI_VMM_DATA_RATE


class Global_cl():
    def __init__(self, input_dict):    
        self.E =  Event_list_cl(self)  # declare event_list, we store event_obj inside
        
        # self.input_dict =dict()
        ### smart input        
        # self.input_dict =input_dict
        
        # self.migration_mode = 'StopNCopy'      # 'PreCopy' or 'StopNCopy'        
        self.migration_mode = input_dict['migration_mode']      # 'PreCopy' or 'StopNCopy'
        
        # self.algo_version = 'StrictSequence'
        self.algo_version = input_dict['algo_version']

        # self.VMmigr_gen_type = input_dict['VMmigr_gen_type']
        #**** VM_first: largest VM search DST first.     
        #**** SRC_first:  smallest SRC --> largest VM search DST first
        self.VMmigr_gen_type = 'vmFirst'        #'VM_first' or 'SRC_first'.  
        
        

        ### smart input        
        
        
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
        if event_obj.time != all_VM__dict[event_obj.vm_num].last_migration_event_finish_time:
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
        self.Initial_upRBW = 0.0   # maybe...useless...Initial residual up BW after all VMM complete  
        self.Initial_dnRBW = 0.0   # maybe...useless...Initial residual down BW after all VMM complete
        self.Final_upRBW = 0.0   # Final residual up BW after all VMM complete
        self.Final_dnRBW = 0.0   # Final residual down BW after all VMM complete
        
        ### tmp varible --> never use this kind of varible for decision making, only if you set varible value by yourself.
        self.upRBW_tmp = 0.0   # now residual up BW
        self.dnRBW_tmp = 0.0   # now residual down BW        
        
        # self.all_VM__dict = dict()  #dict to record VM inside the host
        
        self.waiting_vm__set = set()  # set() to record the  vm_num (waiting migration)
        self.sending_vm__set = set()  # set() to record the  vm_num (sending migration)
        
        self.reg_q__Set = set()   # set() to record the vm_num waiting for migrations with registration
        
        self.GPNum_to_VM__dict = dict()
        for i in GP__set:
            self.GPNum_to_VM__dict[i] = set()   # key: group number   value: VM_obj set

### take care of final_RBW in LB case!!!
    def update(self, vm_upSBW, vm_dnSBW, vm_sigma, migr_type):
        self.upBW += vm_upSBW
        self.dnBW += vm_dnSBW
        self.sigma += vm_sigma
        
        self.upRBW = self.BWC - self.upBW
        self.dnRBW = self.BWC - self.dnBW
        self.Initial_upRBW = self.BWC - self.upBW
        self.Initial_dnRBW = self.BWC - self.dnBW
        
        if migr_type == 'LoadBalancing':
            self.Final_upRBW = self.BWC - self.upBW
            self.Final_dnRBW = self.BWC - self.dnBW


        
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
        
        self.latest_data_rate = 0.0
        self.tmp_rate = 0.0       # tmp rate --> for coding efficiency. no actually power
        
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
        self.last_migration_event_schedule_time = 0  #record the event schedule time
        
        
        
        
        
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

            

### for all parallel algo. --> vm rate may change during migraton proceedings
    def adjust_VM_BW(self, rate):  
    
        # update  vm_obj.remain_size according latest_data_rate 
        last_round_migration_period = self.G.now - self.last_migration_event_schedule_time
        self.remain_size -= float(last_round_migration_period) * self.latest_data_rate
    
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
                
        ### schedule Event_cl() into event list
        finish_time = self.compute_finish_time()
        tmp_info__dict = dict()
        tmp_type = 'vm_finish'
        event_obj = Event_cl(self.G, tmp_type, finish_time, self.vm_num, tmp_info__dict)
        
        assert (self.migration_start_time != 0)        
        self.G.E.list.insert(event_obj)
        

    def release_BW(self):   # release the BW usage.   SRC release uplink, DST release dnlink
        assert (self.status == 'sending')
        
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
        if self.G.algo_version == 'StrictSequence':
            init_func.func_SS_update_ongoing(self.G,self.vm_num)
            ### can change to multiple SS G functions
            func.func_SS(self.G, 1, 'random')
            func.func_SS(self.G, 2, 'random')
        elif G.algo_version == 'ConCurrent':
            ConCur_py.func_Concurrent(self.G, initFlag = False)
        
        
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
        event_obj = Event_cl(self.G, tmp_type, finish_time, self.vm_num, tmp_info__dict)
        
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
        
        if minRate == 0 or minRate <= ACCEPTABLE_MINI_VMM_DATA_RATE:
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
    def __init__(self, G, type, time, vm_num, info__dict = dict()):
        self.G = G
        self.type = type
        self.time = time        #event finish time
        self.event_schedule_time = G.now        #time: schedule the event
        self.vm_num = vm_num
        self.info__dict = info__dict
        
        self.write_time_to_vm_obj()
        
    def write_time_to_vm_obj(self):
        vm_obj = G.all_VM__dict[vm_num]
        vm_obj.last_migration_event_finish_time = self.time
        vm_obj.last_migration_event_schedule_time = self.G.now
        if vm_obj.migration_start_time == 0:
            vm_obj.migration_start_time = self.G.now        
        
