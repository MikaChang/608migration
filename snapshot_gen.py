#-*- coding: utf-8 -*-　
import math
import random

from basic import *

def migr_gen_C(type, vm_num_count, src_num, all_host__dict, all_VM__dict, src__dict):
    if type == 'vmFirst':
        vm__list = range(vm_num_count) # all the vm_num
        ### sorted by each VM's sigma+upSBW+dnSBW
        vm__list = sorted(vm__list, key = lambda vm_num: all_VM__dict[vm_num].sigma + all_VM__dict[vm_num].upSBW + all_VM__dict[vm_num].dnSBW, reverse = True)
        
        dst__list = range(src_num, vm_num_count) # all the DSTnum
        ### sorted by each host's sigma+upBW+dnBW
        dst__list = sorted(dst__list, key = lambda host_num: all_host__dict[host_num].upBW + all_host__dict[host_num].dnBW + all_host__dict[host_num].sigma, reverse = True)
        
        for aVM in vm__list:
            vm_obj = all_VM__dict[aVM]
            for aHost in dst__list:
                dst_obj = all_host__dict[aHost]
                
                if (dst_obj.upBW + vm_obj.upSBW < dst_obj.BWC) & \
                (dst_obj.dnBW + vm_obj.dnSBW < dst_obj.BWC) & \
                (dst_obj.sigma + vm_obj.sigma < dst_obj.sigmaC):
                    vm_obj.DSTnum = aHost
                    dst_obj.Final_upRBW -= vm_obj.upSBW
                    dst_obj.Final_dnRBW -= vm_obj.dnSBW
                    ###下面這兩行是LB case才需要加
                    #all_host__dict[vm_obj.SRCnum].Final_upRBW -= vm_obj.upSBW
                    #all_host__dict[vm_obj.SRCnum].Final_dnRBW -= vm_obj.dnSBW
                    break
                else:
                    continue
    
    elif type == 'srcFirst':
        None
    
    else:
        assert(0)
    
    for aVM in vm__list:
        if all_VM__dict[aVM].DSTnum == None: # 'There is a VM havnt alloc to DST since all the DSTs are full'
            return False
    
    return True
    
def migr_gen_LB():
    None

def snapshot_gen(G, tot_host_num, src_num, migr_type):
    ### tot_host_num can be 16 or 64
    ### src_num can be [4, 8, 12] in 16_mode
    ### migr_type can be 'Consolidation' or 'LoadBalancing'
    
    all_host__dict = dict()
    all_VM__dict = dict()
    src__dict = dict()
    
    ### parameters about VM
    vm_upSBW_range = (2, 8)
    vm_dnSBW_range = (2, 8)
    vm_sigma_range = (2, 8)
    vm_ori_size_range = (30, 80) # GB
    
    ### parameters about host source limit
    if migr_type == 'Consolidation':
        src_upBWC_range = (5, 30) # the unit is percentage
        src_dnBWC_range = (5, 30)
        src_sigmaC_range = (5, 30)
        dst_upBWC_range = (30, 75)
        dst_dnBWC_range = (30, 75)
        dst_sigmaC_range = (30, 75)
    elif migr_type == 'LoadBalancing':
        src_upBWC_range = (75, 95)
        src_dnBWC_range = (75, 95)
        src_sigmaC_range = (75, 95)
        dst_upBWC_range = (30, 50)
        dst_dnBWC_range = (30, 50)
        dst_sigmaC_range = (30, 50)
    else:
        assert(0)
        
    vm_num_count = 0
        
    for i in range(tot_host_num):
        if i < src_num: # SRC 
            src__dict[i] = list()
            host_obj = Host_cl(G, 'SRC', i)
            
            src_upBWC = random.uniform(src_upBWC_range[0], src_upBWC_range[1])
            src_dnBWC = random.uniform(src_dnBWC_range[0], src_dnBWC_range[1])
            src_sigmaC = random.uniform(src_sigmaC_range[0], src_sigmaC_range[1])
            
            while 1:
                vm_upSBW = random.uniform(vm_upSBW_range[0], vm_upSBW_range[1])
                vm_dnSBW = random.uniform(vm_dnSBW_range[0], vm_dnSBW_range[1])
                vm_sigma = random.uniform(vm_sigma_range[0], vm_sigma_range[1])
                vm_ori_size = random.uniform(vm_ori_size_range[0], vm_ori_size_range[1])
                
                if (host_obj.upBW + vm_upSBW <= src_upBWC) &\
                (host_obj.dnBW + vm_dnSBW <= src_dnBWC) &\
                (host_obj.sigma + vm_sigma <= src_sigmaC):
                    
                    vm_obj = VM_cl2(G, vm_ori_size, vm_num_count, vm_upSBW, vm_dnSBW, vm_sigma, i)
                    host_obj.update(vm_upSBW, vm_dnSBW, vm_sigma, 'Consolidation')
                    
                    all_VM__dict[vm_num_count] = vm_obj
                    src__dict[i].append(vm_num_count)
                else:
                    break
                vm_num_count += 1 # equals to exact vm_number - 1

            ###亂數產生host特性限制
            ###亂數產生VM
            ###確定符合條件再加入host(包含update state)還有all_VM__dict還有src__dict(值為list，裡面裝vm_num)
            
        else: # DST
            host_obj = Host_cl(G, 'DST', i)
            
            dst_upBWC = random.uniform(dst_upBWC_range[0], dst_upBWC_range[1])
            dst_dnBWC = random.uniform(dst_dnBWC_range[0], dst_dnBWC_range[1])
            dst_sigmaC = random.uniform(dst_sigmaC_range[0], dst_sigmaC_range[1])
            
            while 1:
                vm_upSBW = random.uniform(vm_upSBW_range[0], vm_upSBW_range[1])
                vm_dnSBW = random.uniform(vm_dnSBW_range[0], vm_dnSBW_range[1])
                vm_sigma = random.uniform(vm_sigma_range[0], vm_sigma_range[1])
                vm_ori_size = random.uniform(vm_ori_size_range[0], vm_ori_size_range[1])
                
                if (host_obj.upBW + vm_upSBW <= src_upBWC) &\
                (host_obj.dnBW + vm_dnSBW <= src_dnBWC) &\
                (host_obj.sigma + vm_sigma <= src_sigmaC):
                    host_obj.update(vm_upSBW, vm_dnSBW, vm_sigma, 'Consolidation')
                else:
                    break
            ###亂數產生host特性限制 
            ###亂數產生VM參數(不做instance)(因為用不到)
            ###確定符合條件就update host參數
        
        all_host__dict[i] = host_obj
    
    if migr_type == 'Consolidation':
        # result = True or False : indicating whether the snapshot is successfully generated or not
        result = migr_gen_C(G.VMmigr_gen_type, vm_num_count, src_num, all_host__dict, all_VM__dict, src__dict)
    else: # LB case
        migr_gen_LB()
    
    return result, all_VM__dict, all_host__dict
    
    ###扔進演算法中計算snapshot#2
    ######SerCon
    ######在每個src_set中掃過每個VM，記錄各VM之sigma順便加總，做成新的score_dict
    ######對src sorting，開始塞
    ######一旦塞成功就更新DSTnum
    ######可能會有1. VM沒塞完  或是2. 有server沒被塞到VM之情況發生，要特別紀錄
    
    ######還要update DST的final_RBW (SRC也要update in LB case)
