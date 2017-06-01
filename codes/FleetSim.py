# -*- coding: utf-8 -*-
"""
@author: Yunshi Zhao
"""
from SimPy.Simulation import *
import random
import math
import csv


class inputs():
    num_parts = 2
    num_ac = [10, 50, 100, 500, 1000]
    total_ac=sum(num_ac)
    pct_simultaneous_repairs = 1.
    repair_people = [0]*len(num_ac)
    for I in range(len(num_ac)):
        repair_people[I] = round(pct_simultaneous_repairs*num_ac[I],0)
    MFHBRRDict = {}
    MFHBRRDict['MFHBRR1'] = [20., 30., 20., 30., 40.]
    MFHBRRDict['MFHBRR2'] = [40., 60., 40., 60., 80.]
    MFHBMEDict = {}
    MFHBMEDict['MFHBME1'] = [10., 20., 10., 20., 10.]
    MFHBMEDict['MFHBME2'] = [20., 40., 20., 40., 30.]
    MFHBRDict = {}
    MFHBRDict['MFHBR1'] = [15., 15., 15., 15., 15.]
    MFHBRDict['MFHBR2'] = [55., 55., 55., 55., 55.]
    MTTRDict = {}
    MTTRDict['MTTR1'] = [5., 5., 5., 5., 5.]
    MTTRDict['MTTR2'] = [3., 3., 3., 3., 3.]
    global_repair_TATDict = {}
    global_repair_TATDict['TAT1'] = [260., 240., 260., 240., 260.]
    global_repair_TATDict['TAT2'] = [210., 260., 210., 260., 260.]
    global_ship_local = [168., 168., 168., 168., 168.]
    global_ship_pool = [96., 72., 72.]
    pool_assignment = [0,0,1,1,2]   
    local_wait_mod = [5., 5., 5., 5., 5.] 
    pool_local_wait_mod = [48., 24., 48., 48., 48.]
    begin_sorties = 0
    end_sorties = 24
    sortie_sched = [1, 1, 1, 1, 1, 0, 0]
    flight_hour_requirement = {}
    flight_hour_requirement['day0'] = [18,108,204,896,1905]
    flight_hour_requirement['day1'] = [18,108,204,896,1905]
    flight_hour_requirement['day2'] = [18,108,204,896,1905]
    flight_hour_requirement['day3'] = [18,108,204,896,1905]
    flight_hour_requirement['day4'] = [18,108,204,896,1905]
    flight_hour_requirement['day5'] = [0, 0, 0, 0, 0]
    flight_hour_requirement['day6'] = [0, 0, 0, 0, 0]
    flight_hours_flown = [0]*len(num_ac)
    flight_hour_per_sortie = [2.0]*len(num_ac)    
    training_surge_toggle = 0
    combat_surge_toggle = 1
    training_surge_time = [0.,43800.]
    training_surge_level = [1.]
    training_surge_countries = [1,1,1,1,1]
    training_surge_AC = [10,10,10,10,10]
    combat_surge_time = [11520.,	12239.]
    combat_surge_level = [2.]
    combat_surge_countries = [0,1,1,1,1]
    combat_surge_AC = [0,5,10,50,100]
    begin_repair = 0
    end_repair = 24
    repair_sched = [1, 1, 1, 1, 1, 0, 0]
    ao_aclevel_file = {}
    ao_countrylevel_file = open('AoVerification_CountryLevel.csv', 'wb')
    ro_countrylevel_file = open('RoVerification_CountryLevel.csv', 'wb')
    partnumber_file = csv.writer(open('PartNumberVerification.csv', 'wb'))
    header_string2 = 'Day'
    for I in range(len(num_ac)):
        header_string2 = header_string2 + ',Available_All_' + str(I+1) + ',Flying_All_' + str(I+1) + ',WaitForRepair_All_' + str(I+1) + ',WaitForPart_All_' + str(I+1) + ',Repair_All_' + str(I+1) + ',Ao_All_' + str(I+1)
        header_string2 = header_string2 + ',Available_Training_' + str(I+1) + ',Flying_Training_' + str(I+1) + ',WaitForRepair_Training_' + str(I+1) + ',WaitForPart_Training_' + str(I+1) + ',Repair_Training_' + str(I+1) + ',Ao_Training_' + str(I+1)
        header_string2 = header_string2 + ',Available_Combat_' + str(I+1) + ',Flying_Combat_' + str(I+1) + ',WaitForRepair_Combat_' + str(I+1) + ',WaitForPart_Combat_' + str(I+1) + ',Repair_Combat_' + str(I+1) + ',Ao_Combat' + str(I+1)
    ao_countrylevel_file.write(header_string2+'\n')
    header_string3 = 'Day'
    for I in range(len(num_ac)):
        header_string3 = header_string3  + ',TrainingRequired_' + str(I+1) + ',TrainingAssigned_' + str(I+1) + ',TrainingCompleted_' + str(I+1) + ',CombatRequired_' + str(I+1) + ',CombatAssigned_' + str(I+1) + ',CombatCompleted_' + str(I+1)
    header_string4=[]
    for I in range(max(pool_assignment)+1):
        for J in range(num_parts):
            header_string4.append('pool'+str(I)+'part'+str(J))
    for I in range(max(pool_assignment)+1):
        for J in range(num_parts):
            header_string4.append('pool_transit'+str(I)+'part'+str(J))
    for I in range(len(num_ac)):
        for J in range(num_parts):
            header_string4.append('training_local'+str(I)+'part'+str(J))
    for I in range(len(num_ac)):
        for J in range(num_parts):
            header_string4.append('local_transit'+str(I)+'part'+str(J))
    for J in range(num_parts):
        header_string4.append('Combat_local'+'part'+str(J))
    for J in range(num_parts):
        header_string4.append('Combat_transit'+'part'+str(J))
    for I in range(len(num_ac)):
        for J in range(num_parts):
            header_string4.append('broken'+str(I)+'part'+str(J))
    for J in range(num_parts):
        header_string4.append('being_repaired'+'part'+str(J))
    for J in range(num_parts):
        header_string4.append('repaired'+'part'+str(J))        
    for J in range(num_parts):
        header_string4.append('in_transit_going'+'part'+str(J))
    for J in range(num_parts):
        header_string4.append('in_transit_coming'+'part'+str(J))
    for I in range(len(num_ac)):     
        for J in range(num_parts):
            header_string4.append('ACBrokenPartsCountry'+str(I)+'part'+str(J))
        for J in range(num_parts):
            header_string4.append('ACCombatBrokenPartsCountry'+str(I)+'part'+str(J))
    partnumber_file.writerow(header_string4)


#define some helper functions to replace numpy
def loggam(x):
    a = [8.333333333333333e-02,-2.777777777777778e-03,
         7.936507936507937e-04,-5.952380952380952e-04,
         8.417508417508418e-04,-1.917526917526918e-03,
         6.410256410256410e-03,-2.955065359477124e-02,
         1.796443723688307e-01,-1.39243221690590e+00]
    
    x0 = x
    n = 0
    if((x == 1.0) or (x == 2.0)):
        return 0.0
    elif (x <= 7.0):
        n = int(7 - x)
        x0 = x + n
    x2 = 1.0/(x0 * x0)
    xp = 2 * math.pi
    g10 = a[9]
    for k in xrange(8,0,-1):
        g10 = g10 * x2
        g10 = g10 + a[k]

    g1 = g10/x0 + 0.5 * math.log(xp) + (x0 - 0.5) * math.log(x0) - x0
    if(x <= 7.0):
        for k in xrange(1,n):
            g1 = g1 - math.log(x0-1.0)
            x0 = x0 - 1.0
    
    return g1

def poisson_ptrs(lam):
    
    slam = lam**0.5
    loglam = math.log(lam)
    b = 0.931 + 2.53*slam
    a = -0.059 + 0.02483 * b
    invalpha = 1.1239 + 1.1328/(b-3.4)
    vr = 0.9277 - 3.6224/(b-2)
    
    while 1:
        U = random.random() - 0.5
        V = random.random()
        us = 0.5 - math.fabs(U)
        k = math.floor((2*a/us + b) * U + lam + 0.43)
        k = int(k)
        if ((us >= 0.07) and (V <= vr)):
            return k
        elif ((k < 0) or ((us < 0.013) and (V > us))):
            continue
        elif ((math.log(V) + math.log(invalpha) - math.log(a/(us*us)+b)) <= (-lam + k*loglam - loggam(k+1))):
            return k
        
def poisson_mult(lam):
    enlam = math.exp(-lam)
    x = 0
    prod = 1.0
    while 1:
        U = random.random()
        prod = prod * U
        if(prod > enlam):
            x = x + 1
        else:
            return x
        
def poisson(lam):
    
    if lam >= 10:
        return poisson_ptrs(lam)
    elif lam == 0:
        return 0
    else:
        return poisson_mult(lam)

def roll(inputArray, places):
    d = deque(inputArray)
    d.rotate(places)
    return list(d)

#Repair person refers to the number of aircraft that can be fixed simultaneously, not actual repair staff
class G:
    Rnd = random.Random()
    RepairFacility = {}
    for I in range(len(inputs.num_ac)):
        RepairFacility['RP' + str(I)] = Resource(inputs.repair_people[I])

#This process sets up sortie generation for each country
class SortieGen(Process):
    SortieDict = {}
    for I in range(len(inputs.num_ac)):
        SortieDict['SortieList' + str(I)] = []
        for J in range(inputs.num_ac[I] + 1):
            SortieDict['HistList' + str(I) + '-' + str(J)] = 0
    def __init__(self,country):
        Process.__init__(self)
        self.country = country
        self.training_sorties_flown = 0
        self.training_sorties_flown_daily = 0
        self.combat_sorties_flown = 0
        self.combat_sorties_flown_daily = 0
        SortieGen.SortieDict['SortieList' + str(self.country)].append(self)
        self.training_required = 0
        self.combat_required = 0
        self.training_sortie_flown = 0
        self.combat_sortie_flown = 0
        self.holdlength = 1
        self.combat_AC_count = 0
    def Run(self):
        while 1:
            if now() == 0:
                self.training_sortie_count  = 0
                self.combat_sortie_count = 0
            if now()%24 == 0:
                self.training_sortie_count  = 0
                self.combat_sortie_count = 0
                for I in range(7):
                    if (now()/24)%7 == I and inputs.sortie_sched[I] == 1:
                        yield hold, self, inputs.begin_sorties
                        if inputs.training_surge_toggle == 1:
                            for J in range(len(inputs.training_surge_time)/2):
                                if now() >= inputs.training_surge_time[2*J] and now() <= inputs.training_surge_time[2*J+1]:
                                    if inputs.training_surge_countries[self.country] == 1:      
                                        self.training_sortie_count = int(round(inputs.flight_hour_requirement['day' + str(I)][self.country]/inputs.num_ac[self.country],0))*inputs.training_surge_AC[self.country]*inputs.training_surge_level[J]
                                    else:
                                        self.training_sortie_count = 0
                                        self.training_sortie_count += inputs.flight_hour_requirement['day' + str(I)][self.country]
                                else:
                                    self.training_sortie_count = 0
                                    self.training_sortie_count += inputs.flight_hour_requirement['day' + str(I)][self.country]
                        else:
                            self.training_sortie_count = 0
                            self.training_sortie_count += inputs.flight_hour_requirement['day' + str(I)][self.country]
                        if inputs.combat_surge_toggle ==1:
                            for J in range(len(inputs.combat_surge_time)/2):
                                if now() >= inputs.combat_surge_time[2*J] and now() <= inputs.combat_surge_time[2*J+1]:
                                    if inputs.combat_surge_countries[self.country] == 1:
                                        self.combat_sortie_count = int(round(inputs.flight_hour_requirement['day' + str(I)][self.country]*inputs.combat_surge_AC[self.country]*inputs.combat_surge_level[J]/inputs.num_ac[self.country],0))
                    elif (now()/24)%7 == I and inputs.sortie_sched[I] == 0:
                        self.holdlength = 24
                        self.training_sortie_count = 0
                        self.combat_sortie_count = 0                        
                self.training_required = 0
                self.combat_required = 0
                self.training_required += self.training_sortie_count
                self.combat_required += self.combat_sortie_count
            if now()%24 < inputs.end_sorties:
                if inputs.combat_surge_toggle ==1:
                    if now() >= inputs.combat_surge_time[0]-24*7 and self.combat_AC_count < inputs.combat_surge_countries[self.country]:                            
                        for K in range(inputs.combat_surge_AC[self.country] - self.combat_AC_count):
                            if len(AC.ACDict['ACtrainingAvailable' + str(self.country)]) == 0:
                                break                            
                            self.temp=AC.ACDict['ACtrainingAvailable' + str(self.country)].pop()
                            self.temp.mission_type = 'combat'
                            AC.ACDict['ACcombatAvailable' + str(self.country)].append(self.temp)
                            self.combat_AC_count += 1
                    if now() >= inputs.combat_surge_time[len(inputs.combat_surge_time)-1] and (len(AC.ACDict['ACcombatAvailable' + str(self.country)]) > 0 or len(AC.ACDict['ACcombatNeedPart' + str(self.country)]) > 0):
                        for K in range(len(AC.ACDict['ACcombatAvailable' + str(self.country)])):
                            self.temp=AC.ACDict['ACcombatAvailable' + str(self.country)].pop()
                            self.temp.mission_type = 'training'
                            AC.ACDict['ACtrainingAvailable' + str(self.country)].append(self.temp)
                        for K in range(len(AC.ACDict['ACcombatNeedPart' + str(self.country)])):
                            self.temp=AC.ACDict['ACcombatNeedPart' + str(self.country)].pop()
                            self.temp.mission_type = 'training'
                            AC.ACDict['ACtrainingNeedPart' + str(self.country)].append(self.temp)
                while self.training_sortie_count > 0:
                    if len(AC.ACDict['ACtrainingAvailable' + str(self.country)]) == 0:
                        break
                    if AC.ACDict['ACtrainingAvailable' + str(self.country)][0].passivated==0:  
                        reactivate(AC.ACDict['ACtrainingAvailable' + str(self.country)][0])
                        del AC.ACDict['ACtrainingAvailable' + str(self.country)][0]
                        self.training_sortie_count -= 1
                while self.combat_sortie_count > 0:
                    if len(AC.ACDict['ACcombatAvailable' + str(self.country)]) == 0:
                        break
                    if AC.ACDict['ACcombatAvailable' + str(self.country)][0].passivated==0:  
                        reactivate(AC.ACDict['ACcombatAvailable' + str(self.country)][0])
                        del AC.ACDict['ACcombatAvailable' + str(self.country)][0]
                        self.combat_sortie_count -= 1
            yield hold, self, self.holdlength
            self.holdlength = 1

#This process tells each aircraft what to do
class AC(Process):
    ACDict = {}
    for I in range(len(inputs.num_ac)):
        ACDict['ACList' + str(I)] = []
        ACDict['ACtrainingAvailable' + str(I)] = []
        ACDict['ACtrainingNeedPart' + str(I)] = []
        ACDict['ACcombatAvailable' + str(I)] = []
        ACDict['ACcombatNeedPart' + str(I)] = []
    ID_count = 0
    BrokenParts={}
    combatBrokenParts={}
    for I in range(inputs.num_parts):
        BrokenParts['part' + str(I)] = [0]*len(inputs.num_ac)
        combatBrokenParts['part' + str(I)] = [0]*len(inputs.num_ac)     
    def __init__(self,country):
        Process.__init__(self)
        self.country = country
        self.ID = AC.ID_count
        AC.ID_count += 1
        AC.ACDict['ACList' + str(self.country)].append(self)
        AC.ACDict['ACtrainingAvailable' + str(self.country)].append(self)
        self.mission_time = 0
        self.maintenance_events_this_flight = [0]*inputs.num_parts
        for I in range(inputs.num_parts):
            self.maintenance_events_this_flight[I] = poisson(inputs.flight_hour_per_sortie[self.country]/inputs.MFHBMEDict['MFHBME' + str(I+1)][self.country])
        self.total_flying_time = 0
        self.total_available_time = 0
        self.total_BWR_time = 0
        self.total_BWP_time = 0
        self.total_BBR_time = 0
        self.flying_time_today = 0
        self.available_time_today = 0
        self.BAR_time_today = 0
        self.BAP_time_today = 0
        self.BBR_time_today = 0
        self.required_removal_events_part = [0]*inputs.num_parts
        self.passivated = 0
        self.tprev = 0
        self.state = 0
        self.cumulative_me = [0]*inputs.num_parts
        self.cumulative_r = [0]*inputs.num_parts
        self.number_of_parts_broken_this_flight = [0]*inputs.num_parts
        self.daily_missions = 0
        self.mission_type = 'training'
        self.broken=[0]*inputs.num_parts
    def Run(self):
        while 1:
            self.state = 0
            self.tprev = now()
            self.passivated=0    
            yield passivate, self
            if self.state == 0:
                self.total_available_time += now() - self.tprev
                self.available_time_today += now() - self.tprev
            elif self.state == 1:
                self.total_flying_time += now() - self.tprev
                self.flying_time_today += now() - self.tprev
            elif self.state == 2:
                self.total_BWR_time += now() - self.tprev
                self.BAR_time_today += now() - self.tprev
            elif self.state == 3:
                self.total_BWP_time += now() - self.tprev
                self.BAP_time_today += now() - self.tprev
            elif self.state == 4:
                self.total_BBR_time += now() - self.tprev
                self.bbr_time_today += now() - self.tprev
            self.daily_missions += 1		
            self.critical_failure = [0]*inputs.num_parts
            for I in range(inputs.num_parts):
                self.maintenance_events_this_flight[I] = poisson(inputs.flight_hour_per_sortie[self.country]/inputs.MFHBMEDict['MFHBME' + str(I+1)][self.country])
                self.number_of_parts_broken_this_flight[I] = poisson(inputs.flight_hour_per_sortie[self.country]/inputs.MFHBRDict['MFHBR' + str(I+1)][self.country])              
                for J in range(self.maintenance_events_this_flight[I]):
                    if random.uniform(0.,1.) < inputs.MFHBMEDict['MFHBME' + str(I+1)][self.country]/inputs.MFHBRRDict['MFHBRR' + str(I+1)][self.country]:
                        self.critical_failure[I]+=1                   
                self.cumulative_me[I] += self.maintenance_events_this_flight[I]
                self.cumulative_r[I] += self.number_of_parts_broken_this_flight[I]
            self.mission_time = inputs.flight_hour_per_sortie[self.country]
            self.state=1
            self.tprev = now()              
            yield hold, self, self.mission_time
            inputs.flight_hours_flown[self.country] = inputs.flight_hours_flown[self.country] + self.mission_time                
            if self.state == 0:
                self.total_available_time += now() - self.tprev
                self.available_time_today += now() - self.tprev
            elif self.state == 1:
                self.total_flying_time += now() - self.tprev
                self.flying_time_today += now() - self.tprev
            elif self.state == 2:
                self.total_BWR_time += now() - self.tprev
                self.BAR_time_today += now() - self.tprev
            elif self.state == 3:
                self.total_BWP_time += now() - self.tprev
                self.BAP_time_today += now() - self.tprev
            elif self.state == 4:
                self.total_BBR_time += now() - self.tprev
                self.BBR_time_today += now() - self.tprev
            if self.mission_type == 'training':
                SortieGen.SortieDict['SortieList' + str(self.country)][0].training_sortie_flown += 1
            elif self.mission_type == 'combat':
                SortieGen.SortieDict['SortieList' + str(self.country)][0].combat_sortie_flown += 1
            self.state = 0
            self.tprev = now()
            if max(self.critical_failure) > 0:
                self.broken=[0]*inputs.num_parts
                for I in range(inputs.num_parts):
                    self.broken[I]=self.cumulative_r[I]
                    if self.mission_type == 'training':
                        AC.BrokenParts['part' + str(I)][self.country] = AC.BrokenParts['part' + str(I)][self.country]+self.cumulative_r[I]
                    elif self.mission_type == 'combat':
                        AC.combatBrokenParts['part' + str(I)][self.country] = AC.combatBrokenParts['part' + str(I)][self.country]+self.cumulative_r[I]
                if self.mission_type == 'training':
                    AC.ACDict['ACtrainingNeedPart' + str(self.country)].append(self) 
                elif self.mission_type == 'combat':
                    AC.ACDict['ACcombatNeedPart' + str(self.country)].append(self)                 
                for I in range(inputs.num_parts):
                    for J in range(self.broken[I]):
                        self.temp=inventoryclassDict[str(I)].Iven_PartDict['equip_ac'+str(self.ID)].pop()
                        inventoryclassDict[str(I)].Iven_PartDict['broken'+str(self.country)].append(self.temp)
                max_repair_time = 0
                for I in range(inputs.num_parts):
                    if self.cumulative_me[I] > 0:
                        max_repair_time = max(max_repair_time,inputs.MTTRDict['MTTR' + str(I+1)][self.country])
                if sum(self.broken) == 0:
                    self.passivated = 0
                    self.tprev = now()
                    self.state = 0
                else:
                    self.state = 3
                    self.tprev = now()
                    self.passivated = 1
                    yield passivate, self
                if self.state == 0:
                    self.total_available_time += now() - self.tprev
                    self.available_time_today += now() - self.tprev
                elif self.state == 1:
                    self.total_flying_time += now() - self.tprev
                    self.flying_time_today += now() - self.tprev
                elif self.state == 2:
                    self.total_BWR_time += now() - self.tprev
                    self.BAR_time_today = now() - self.tprev
                elif self.state == 3:
                    self.total_BWP_time += now() - self.tprev
                    self.BAP_time_today += now() - self.tprev
                elif self.state == 4:
                    self.total_BBR_time += now() - self.tprev
                    self.BBR_time_today += now() - self.tprev
                self.state = 2
                self.tprev = now()
                yield request, self, G.RepairFacility['RP' + str(self.country)]
                if self.state == 0:
                    self.total_available_time += now() - self.tprev
                    self.available_time_today += now() - self.tprev
                elif self.state == 1:
                    self.total_flying_time += now() - self.tprev
                    self.flying_time_today += now() - self.tprev
                elif self.state == 2:
                    self.total_BWR_time += now() - self.tprev
                    self.BAR_time_today += now() - self.tprev
                elif self.state == 3:
                    self.total_BWP_time += now() - self.tprev
                    self.BAP_time_today += now() - self.tprev
                elif self.state == 4:
                    self.total_BBR_time += now() - self.tprev
                    self.BBR_time_today += now() - self.tprev
                self.state = 4
                self.tprev = now()
                yield hold, self, max_repair_time
                if self.state == 0:
                    self.total_available_time += now() - self.tprev
                    self.available_time_today += now() - self.tprev
                elif self.state == 1:
                    self.total_flying_time += now() - self.tprev
                    self.flying_time_today += now() - self.tprev
                elif self.state == 2:
                    self.total_BWR_time += now() - self.tprev
                    self.BAR_time_today += now() - self.tprev
                elif self.state == 3:
                    self.total_BWP_time += now() - self.tprev
                    self.BAP_time_today += now() - self.tprev
                elif self.state == 4:
                    self.total_BBR_time += now() - self.tprev
                    self.BBR_time_today += now() - self.tprev    
                self.state = 0
                self.tprev = now()
                yield release, self, G.RepairFacility['RP' + str(self.country)]
                self.cumulative_me=[0]*inputs.num_parts
                self.cumulative_r=[0]*inputs.num_parts
            self.state = 0
            self.tprev = now()
            if self.mission_type == 'training':
                AC.ACDict['ACtrainingAvailable' + str(self.country)].append(self)
            elif self.mission_type == 'combat':
                AC.ACDict['ACcombatAvailable' + str(self.country)].append(self)

#This process handles the creation of the queue and its management for aircraft that enter the queue concurrently
class Queue(Process):
    parts_queue=[]
    parts_training_queue = []
    parts_combat_queue = []
    def __init__(self):
        Process.__init__(self)
    def Run(self):
        while 1:
            Queue.parts_queue=[]
            parts_training_needed = 0
            training_num_simultaneous = 0
            for I in range(len(inputs.num_ac)):
                if len(AC.ACDict['ACtrainingNeedPart' + str(I)]) > 0:
                    parts_training_needed = 1
                    training_num_simultaneous = training_num_simultaneous + len(AC.ACDict['ACtrainingNeedPart' + str(I)])
            if parts_training_needed == 1:
                sort_training_random = [0]*training_num_simultaneous
                sort_training_ac = [0]*training_num_simultaneous
                training_broken = [0]*len(inputs.num_ac)
                for I in range(len(inputs.num_ac)):
                        training_broken[I] = len(AC.ACDict['ACtrainingNeedPart' + str(I)])
                for I in range(training_num_simultaneous):
                    sort_training_random[I] = random.uniform(0.,1.)
                    for J in range(len(inputs.num_ac)):
                        if I+1 <= sum(training_broken[0:J+1]):
                            sort_training_ac[I] = AC.ACDict['ACtrainingNeedPart' + str(J)][0]
                            del AC.ACDict['ACtrainingNeedPart' + str(J)][0]
                            break
                training_scrambled = zip(*sorted(zip(sort_training_random, sort_training_ac)))[1]
                for I in range(len(training_scrambled)):
                    Queue.parts_training_queue.append(training_scrambled[I])
            parts_combat_needed = 0
            combat_num_simultaneous = 0
            for I in range(len(inputs.num_ac)):
                if len(AC.ACDict['ACcombatNeedPart' + str(I)]) > 0:
                    parts_combat_needed = 1
                    combat_num_simultaneous = combat_num_simultaneous + len(AC.ACDict['ACcombatNeedPart' + str(I)])
            if parts_combat_needed == 1:
                sort_combat_random = [0]*combat_num_simultaneous
                sort_combat_ac = [0]*combat_num_simultaneous
                combat_broken = [0]*len(inputs.num_ac)
                for I in range(len(inputs.num_ac)):
                        combat_broken[I] = len(AC.ACDict['ACcombatNeedPart' + str(I)])
                for I in range(combat_num_simultaneous):
                    sort_combat_random[I] = random.uniform(0.,1.)
                    for J in range(len(inputs.num_ac)):
                        if I+1 <= sum(combat_broken[0:J+1]):
                            sort_combat_ac[I] = AC.ACDict['ACcombatNeedPart' + str(J)][0]
                            del AC.ACDict['ACcombatNeedPart' + str(J)][0]
                            break
                combat_scrambled = zip(*sorted(zip(sort_combat_random, sort_combat_ac)))[1]
                for I in range(len(combat_scrambled)):
                    Queue.parts_combat_queue.append(combat_scrambled[I])
            Queue.parts_queue.append(Queue.parts_combat_queue)
            Queue.parts_queue.append(Queue.parts_training_queue)
            if now()%24==0:
                print 'Day', now()/24
            yield hold, self, 1

#This process handles the spare part cycle for each country
class Parts(Process):
    def __init__(self):
        Process.__init__(self)
    def Run(self):
        while 1:
            if now()%24 > inputs.begin_repair and now()%24 < inputs.end_repair:
                for I in range(inputs.num_parts):
                    for J in range(len(inputs.num_ac)):
                        while len(inventoryclassDict[str(I)].Iven_PartDict['broken'+str(J)]) > 0:
                            self.temp=inventoryclassDict[str(I)].Iven_PartDict['broken'+str(J)].pop()
                            inventoryclassDict[str(I)].Iven_PartDict['in_transit_going'].append(self.temp)
                            S = Send(J,I)
                            activate(S,S.Run())                        
                for Z in range(len(Queue.parts_queue)):            
                    if len(Queue.parts_queue[Z]) > 0:
                        I_delete = 0
                        for I in range(len(Queue.parts_queue[Z])):
                            check=0
                            for J in range(inputs.num_parts):
                                if Queue.parts_queue[Z][I-I_delete].broken[J] > 0:
                                    if Queue.parts_queue[Z][I-I_delete].mission_type == 'combat':
                                        if len(inventoryclassDict[str(J)].Iven_PartDict['combat_local']) >= Queue.parts_queue[Z][I-I_delete].broken[J]:
                                            for K in range(Queue.parts_queue[Z][I-I_delete].broken[J]):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type+'_local'].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['combat_transit'].append(self.temp)                                            
                                                OPC = OrderPC(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPC,OPC.Run())                                 
                                                CLTT = Combat_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(CLTT,CLTT.Run())
                                            Queue.parts_queue[Z][I-I_delete].broken[J] = 0
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local']) > 0 and len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) >= Queue.parts_queue[Z][I-I_delete].broken[J] - len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local']):
                                            for K in range(Queue.parts_queue[Z][I-I_delete].broken[J] - len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'])):                          
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)                                          
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                                                                      
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_transit'].append(self.temp)                                             
                                                OPC = OrderPC(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPC,OPC.Run())                                                                               
                                                CLTT = Combat_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(CLTT,CLTT.Run())
                                            Queue.parts_queue[Z][I-I_delete].broken[J] = 0
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) >= Queue.parts_queue[Z][I-I_delete].broken[J]:
                                            for K in range(Queue.parts_queue[Z][I-I_delete].broken[J]):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)                                              
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                                                                      
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                            Queue.parts_queue[Z][I-I_delete].broken[J] = 0
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local']) > 0 and len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) > 0:
                                            Queue.parts_queue[Z][I-I_delete].broken[J] -= len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local']) + len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)                                             
                                                OPC = OrderPC(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPC,OPC.Run())                                                                                       
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_transit'].append(self.temp)
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                
                                                CLTT = Combat_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(CLTT,CLTT.Run())                                  
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local']) > 0:
                                            Queue.parts_queue[Z][I-I_delete].broken[J] -= len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'])
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_local'].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict[Queue.parts_queue[Z][I-I_delete].mission_type + '_transit'].append(self.temp)                                            
                                                OPC = OrderPC(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPC,OPC.Run())                                                                                              
                                                CLTT = Combat_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(CLTT,CLTT.Run())
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) > 0:
                                            Queue.parts_queue[Z][I-I_delete].broken[J] -= len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)                                               
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                                                                        
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                    elif Queue.parts_queue[Z][I-I_delete].mission_type == 'training':
                                        if len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)]) >= Queue.parts_queue[Z][I-I_delete].broken[J]:
                                            for K in range(Queue.parts_queue[Z][I-I_delete].broken[J]):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['local_transit'+str(Queue.parts_queue[Z][I-I_delete].country)].append(self.temp)
                                                OPT = OrderPT(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPT,OPT.Run())                                                                                            
                                                TLTT = Training_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(TLTT,TLTT.Run())
                                            Queue.parts_queue[Z][I-I_delete].broken[J] = 0
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)]) > 0 and len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) >= Queue.parts_queue[Z][I-I_delete].broken[J] - len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)]):
                                            for K in range(Queue.parts_queue[Z][I-I_delete].broken[J] - len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)])):                          
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())         
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['local_transit'+str(Queue.parts_queue[Z][I-I_delete].country)].append(self.temp)
                                                OPT = OrderPT(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPT,OPT.Run())                                                          
                                                TLTT = Training_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(TLTT,TLTT.Run())
                                            Queue.parts_queue[Z][I-I_delete].broken[J] = 0
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) >= Queue.parts_queue[Z][I-I_delete].broken[J]:
                                            for K in range(Queue.parts_queue[Z][I-I_delete].broken[J]):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                                           
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                            Queue.parts_queue[Z][I-I_delete].broken[J] = 0
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)]) > 0 and len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) > 0:
                                            Queue.parts_queue[Z][I-I_delete].broken[J] -= len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)]) + len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                                           
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['local_transit'+str(Queue.parts_queue[Z][I-I_delete].country)].append(self.temp)
                                                OPT = OrderPT(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPT,OPT.Run())                                                            
                                                TLTT = Training_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(TLTT,TLTT.Run())                                   
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)]) > 0:
                                            Queue.parts_queue[Z][I-I_delete].broken[J] -= len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)])
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(Queue.parts_queue[Z][I-I_delete].country)].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['local_transit'+str(Queue.parts_queue[Z][I-I_delete].country)].append(self.temp)
                                                OPT = OrderPT(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OPT,OPT.Run())                                                          
                                                TLTT = Training_Local_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(TLTT,TLTT.Run())
                                        elif len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])]) > 0:
                                            Queue.parts_queue[Z][I-I_delete].broken[J] -= len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])
                                            for K in range(len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])])):
                                                self.temp=inventoryclassDict[str(J)].Iven_PartDict['pool'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].pop()
                                                inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country])].append(self.temp)
                                                OGP = OrderGP(Queue.parts_queue[Z][I-I_delete].country,J)
                                                activate(OGP,OGP.Run())                                                           
                                                PTT = Pool_transit_time(J,Queue.parts_queue[Z][I-I_delete].country,inputs.pool_assignment[Queue.parts_queue[Z][I-I_delete].country],Queue.parts_queue[Z][I-I_delete].ID)
                                                activate(PTT,PTT.Run())
                            check = 0
                            for J in range(inputs.num_parts):
                                check+=len(inventoryclassDict[str(J)].Iven_PartDict['equip_ac'+str(Queue.parts_queue[Z][I-I_delete].ID)])
                            if check == (inputs.num_parts)*100:
                                reactivate(Queue.parts_queue[Z][I-I_delete])
                                del Queue.parts_queue[Z][I-I_delete]
                                I += 1
                                I_delete += 1
            yield hold, self, 1

class inventory0():
    ID_count = 0
    Iven_PartDict={}    
    for I in range(len(inputs.num_ac)):
        Iven_PartDict['training_local'+str(I)]=[]
    Iven_PartDict['combat_local']=[]
    for I in range(len(inputs.num_ac)):
        Iven_PartDict['local_transit'+str(I)] = []
    Iven_PartDict['combat_transit']=[] 
    for I in range(max(inputs.pool_assignment)+1):
        Iven_PartDict['pool'+str(I)]=[]
    for I in range(max(inputs.pool_assignment)+1):
        Iven_PartDict['pool_transit'+str(I)] = []
    Iven_PartDict['global_being_repaired'] = []
    Iven_PartDict['global_available'] = []
    for I in range(len(inputs.num_ac)):
        Iven_PartDict['broken'+str(I)]=[]  
    Iven_PartDict['in_transit_coming']=[]
    Iven_PartDict['in_transit_going']=[]
    for I in range(len(inputs.num_ac)):
        for J in range(inputs.num_ac[I]):
            Iven_PartDict['equip_ac'+str(J+sum(inputs.num_ac[0:I]))]=[]       
    def __init__(self,initial_state,part_number):
        self.initial_state=initial_state
        self.part_number=part_number
        self.ID = inventory0.ID_count
        inventory0.ID_count += 1
        if initial_state[0]=='training_local':
            inventory0.Iven_PartDict['training_local'+str(initial_state[1])].append(self)
        elif initial_state[0]=='combat_local':
            inventory0.Iven_PartDict['combat_local'].append(self)
        elif initial_state[0]=='combat_transit':
            inventory0.Iven_PartDict['combat_transit'].append(self)
        elif initial_state[0]=='local_transit':
            inventory0.Iven_PartDict['local_transit'+str(initial_state[1])].append(self)
        elif initial_state[0]=='pool':
            inventory0.Iven_PartDict['pool'+str(initial_state[1])].append(self)
        elif initial_state[0]=='pool_transit':
            inventory0.Iven_PartDict['pool_transit'+str(initial_state[1])].append(self)
        elif initial_state[0]=='global_repair':
            inventory0.Iven_PartDict['global_being_repaired'].append(self)
        elif initial_state[0]=='global_available':
            inventory0.Iven_PartDict['global_available'].append(self)
        elif initial_state[0]=='broken':
            inventory0.Iven_PartDict['broken'+str(initial_state[1])].append(self)
        elif initial_state[0]=='in_transit_coming':
            inventory0.Iven_PartDict['in_transit_coming'].append(self)
        elif initial_state[0]=='in_transit_going':
            inventory0.Iven_PartDict['in_transit_going'].append(self)
        elif initial_state[0]=='equip_ac':
            inventory0.Iven_PartDict['equip_ac'+str(initial_state[1])].append(self)           
class inventory1():
    ID_count = 0
    Iven_PartDict={}
    
    for I in range(len(inputs.num_ac)):
        Iven_PartDict['training_local'+str(I)]=[]
    Iven_PartDict['combat_local']=[]
    for I in range(len(inputs.num_ac)):
        Iven_PartDict['local_transit'+str(I)] = []
    Iven_PartDict['combat_transit']=[]
    for I in range(max(inputs.pool_assignment)+1):
        Iven_PartDict['pool'+str(I)]=[]
    for I in range(max(inputs.pool_assignment)+1):
        Iven_PartDict['pool_transit'+str(I)] = []
    Iven_PartDict['global_being_repaired'] = []
    Iven_PartDict['global_available'] = []
    for I in range(len(inputs.num_ac)):
        Iven_PartDict['broken'+str(I)]=[]  
    Iven_PartDict['in_transit_coming']=[]
    Iven_PartDict['in_transit_going']=[]
    for I in range(len(inputs.num_ac)):
        for J in range(inputs.num_ac[I]):
            Iven_PartDict['equip_ac'+str(J+sum(inputs.num_ac[0:I]))]=[]  
    def __init__(self,initial_state,part_number):
        self.initial_state=initial_state
        self.part_number=part_number
        self.ID = inventory1.ID_count
        inventory1.ID_count += 1
        if initial_state[0]=='training_local':
            inventory1.Iven_PartDict['training_local'+str(initial_state[1])].append(self)
        elif initial_state[0]=='combat_local':
            inventory1.Iven_PartDict['combat_local'].append(self)
        elif initial_state[0]=='combat_transit':
            inventory1.Iven_PartDict['combat_transit'].append(self)
        elif initial_state[0]=='local_transit':
            inventory1.Iven_PartDict['local_transit'+str(initial_state[1])].append(self)
        elif initial_state[0]=='pool':
            inventory1.Iven_PartDict['pool'+str(initial_state[1])].append(self)
        elif initial_state[0]=='pool_transit':
            inventory1.Iven_PartDict['pool_transit'+str(initial_state[1])].append(self)
        elif initial_state[0]=='global_repair':
            inventory1.Iven_PartDict['global_being_repaired'].append(self)
        elif initial_state[0]=='global_available':
            inventory1.Iven_PartDict['global_available'].append(self)
        elif initial_state[0]=='broken':
            inventory1.Iven_PartDict['broken'+str(initial_state[1])].append(self)
        elif initial_state[0]=='in_transit_coming':
            inventory1.Iven_PartDict['in_transit_coming'].append(self)
        elif initial_state[0]=='in_transit_going':
            inventory1.Iven_PartDict['in_transit_going'].append(self)
        elif initial_state[0]=='equip_ac':
            inventory1.Iven_PartDict['equip_ac'+str(initial_state[1])].append(self)
inventoryclassDict = {}
inventoryclassDict['0'] = inventory0
inventoryclassDict['1'] = inventory1

class Training_Local_transit_time(Process):
    def __init__(self,part,country,ac):
        Process.__init__(self)
        self.part = part
        self.country = country
        self.ac = ac
    def Run(self):
        yield hold, self, inputs.local_wait_mod[self.country]
        self.temp = inventoryclassDict[str(self.part)].Iven_PartDict['local_transit'+str(self.country)].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['equip_ac'+str(self.ac)].append(self.temp)
        
class Combat_Local_transit_time(Process):
    def __init__(self,part,country,ac):
        Process.__init__(self)
        self.part = part
        self.country = country
        self.ac = ac
    def Run(self):
        yield hold, self, inputs.local_wait_mod[self.country]
        self.temp = inventoryclassDict[str(self.part)].Iven_PartDict['combat_transit'].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['equip_ac'+str(self.ac)].append(self.temp)
        
class Pool_transit_time(Process):
    def __init__(self,part,country,pool,ac):
        Process.__init__(self)
        self.part = part
        self.country = country
        self.pool = pool
        self.ac = ac
    def Run(self):
        yield hold, self, inputs.pool_local_wait_mod[self.country]
        self.temp = inventoryclassDict[str(self.part)].Iven_PartDict['pool_transit'+str(self.pool)].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['equip_ac'+str(self.ac)].append(self.temp)

#This process sends parts to be repaired and is activated when needed and only run once
class Send(Process):
    def __init__(self, country, part):
        Process.__init__(self)
        self.country = country
        self.part = part
    def Run(self):
        yield hold, self, inputs.global_ship_local[self.country]
        self.temp = inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_going'].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['global_being_repaired'].append(self.temp)
        yield hold, self, inputs.global_repair_TATDict['TAT' + str(self.part+1)][self.country]
        self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['global_being_repaired'].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['global_available'].append(self.temp)

class OrderPT(Process):
    def __init__(self, country, part):
        Process.__init__(self)
        self.country = country
        self.part = part
    def Run(self):
        while len(inventoryclassDict[str(self.part)].Iven_PartDict['global_available']) == 0 and len(inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])])==0:
            yield hold, self, 1
        if len(inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])]) > 0:
            self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['pool_transit' + str(inputs.pool_assignment[self.country])].append(self.temp)
            OGP = OrderGP(self.country,self.part)
            activate(OGP,OGP.Run())
            yield hold, self, inputs.pool_local_wait_mod[self.country]
            self.temp = inventoryclassDict[str(self.part)].Iven_PartDict['pool_transit'+ str(inputs.pool_assignment[self.country])].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['training_local'+str(self.country)].append(self.temp)
        elif len(inventoryclassDict[str(self.part)].Iven_PartDict['global_available']) > 0:
            #Wait for parts to ship to local inventory location
            self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['global_available'].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_coming'].append(self.temp)
            yield hold, self, inputs.global_ship_local[self.country]
            self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_coming'].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['training_local'+str(self.country)].append(self.temp)

class OrderPC(Process):
    def __init__(self, country, part):
        Process.__init__(self)
        self.country = country
        self.part = part
    def Run(self):
        while len(inventoryclassDict[str(self.part)].Iven_PartDict['global_available']) == 0 and len(inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])])==0:
            yield hold, self, 1
        if len(inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])]) > 0:
            self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['pool_transit' + str(inputs.pool_assignment[self.country])].append(self.temp)
            OGP = OrderGP(self.country,self.part)
            activate(OGP,OGP.Run())
            yield hold, self, inputs.pool_local_wait_mod[self.country]
            self.temp = inventoryclassDict[str(self.part)].Iven_PartDict['pool_transit'+ str(inputs.pool_assignment[self.country])].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['combat_local'].append(self.temp)
        elif len(inventoryclassDict[str(self.part)].Iven_PartDict['global_available']) > 0:
            self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['global_available'].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_coming'].append(self.temp)
            yield hold, self, inputs.global_ship_local[self.country]
            self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_coming'].pop()
            inventoryclassDict[str(self.part)].Iven_PartDict['combat_local'].append(self.temp)

#This process requests parts from the pooled inventory and is activated when needed and only run once
class OrderGP(Process):
    def __init__(self, country, part):
        Process.__init__(self)
        self.country = country
        self.part = part
    def Run(self):
        while len(inventoryclassDict[str(self.part)].Iven_PartDict['global_available']) == 0 :
            yield hold, self, 1
        #Wait for parts to ship to pooled inventory location
        self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['global_available'].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_coming'].append(self.temp)
        yield hold, self, inputs.global_ship_pool[inputs.pool_assignment[self.country]]
        self.temp=inventoryclassDict[str(self.part)].Iven_PartDict['in_transit_coming'].pop()
        inventoryclassDict[str(self.part)].Iven_PartDict['pool'+str(inputs.pool_assignment[self.country])].append(self.temp)            

#This process records quantities daily to be output as time series data
class Daily(Process): 
    def __init__(self):
        Process.__init__(self)
    def Run(self):
        while 1:
            if now()%24 == 0 and now() != 0:
                line_append2 = []
                for I in range(max(inputs.pool_assignment)+1):
                    for J in range(inputs.num_parts):
                        line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['pool'+str(I)]))
                for I in range(max(inputs.pool_assignment)+1):
                    for J in range(inputs.num_parts):
                        line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['pool_transit'+str(I)]))
                for I in range(len(inputs.num_ac)):
                    for J in range(inputs.num_parts):
                        line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['training_local'+str(I)]))
                for J in range(inputs.num_parts):
                    line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['combat_local']))
                for J in range(inputs.num_parts):
                    line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['combat_transit']))
                for I in range(len(inputs.num_ac)):
                    for J in range(inputs.num_parts):
                        line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['local_transit'+str(I)]))
                for I in range(len(inputs.num_ac)):
                    for J in range(inputs.num_parts):
                        line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['broken'+str(I)]))
                for J in range(inputs.num_parts):
                    line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['global_being_repaired']))
                for J in range(inputs.num_parts):
                    line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['global_available']))
                for J in range(inputs.num_parts):
                    line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['in_transit_going']))
                for J in range(inputs.num_parts):
                        line_append2.append(len(inventoryclassDict[str(J)].Iven_PartDict['in_transit_coming']))
                for I in range(len(inputs.num_ac)):     
                    for J in range(inputs.num_parts):
                        line_append2.append(AC.BrokenParts['part' + str(J)][I])
                    for J in range(inputs.num_parts):
                        line_append2.append(AC.combatBrokenParts['part' + str(J)][I])
                inputs.partnumber_file.writerow(line_append2)
                for I in range(len(inputs.num_ac)):
                    for J in range(inputs.num_ac[I]):
                        if AC.ACDict['ACList' + str(I)][J].available_time_today + AC.ACDict['ACList' + str(I)][J].flying_time_today + AC.ACDict['ACList' + str(I)][J].BAR_time_today + AC.ACDict['ACList' + str(I)][J].BAP_time_today + AC.ACDict['ACList' + str(I)][J].BBR_time_today < 24:
                            if AC.ACDict['ACList' + str(I)][J].state == 0:
                                AC.ACDict['ACList' + str(I)][J].available_time_today += now() - AC.ACDict['ACList' + str(I)][J].tprev
                            elif AC.ACDict['ACList' + str(I)][J].state == 1:
                                AC.ACDict['ACList' + str(I)][J].flying_time_today += now() - AC.ACDict['ACList' + str(I)][J].tprev
                            elif AC.ACDict['ACList' + str(I)][J].state == 2:
                                AC.ACDict['ACList' + str(I)][J].BAR_time_today += now() - AC.ACDict['ACList' + str(I)][J].tprev
                            elif AC.ACDict['ACList' + str(I)][J].state == 3:
                                AC.ACDict['ACList' + str(I)][J].BAP_time_today += now() - AC.ACDict['ACList' + str(I)][J].tprev
                            elif AC.ACDict['ACList' + str(I)][J].state == 4:
                                AC.ACDict['ACList' + str(I)][J].BBR_time_today += now() - AC.ACDict['ACList' + str(I)][J].tprev
                            AC.ACDict['ACList' + str(I)][J].tprev = now()                     
                ao_aclevel_string = {}
                ao_aclevel_string[I] = str(now()/24)
                ao_countrylevel_string = str(now()/24)
                ro_countrylevel_string = str(now()/24)
                for I in range(len(inputs.num_ac)):
                    country_available_sum = 0
                    country_flying_sum = 0
                    country_BAR_sum = 0
                    country_BAP_sum = 0
                    country_BBR_sum = 0
                    country_training_available_sum = 0
                    country_training_flying_sum = 0
                    country_training_BAR_sum = 0
                    country_training_BAP_sum = 0
                    country_training_BBR_sum = 0
                    country_combat_available_sum = 0
                    country_combat_flying_sum = 0
                    country_combat_BAR_sum = 0
                    country_combat_BAP_sum = 0
                    country_combat_BBR_sum = 0 
                    for J in range(inputs.num_ac[I]):
                        country_available_sum += AC.ACDict['ACList' + str(I)][J].available_time_today
                        country_flying_sum += AC.ACDict['ACList' + str(I)][J].flying_time_today
                        country_BAR_sum += AC.ACDict['ACList' + str(I)][J].BAR_time_today
                        country_BAP_sum += AC.ACDict['ACList' + str(I)][J].BAP_time_today
                        country_BBR_sum += AC.ACDict['ACList' + str(I)][J].BBR_time_today
                        if AC.ACDict['ACList' + str(I)][J].mission_type == "training":
                            country_training_available_sum += AC.ACDict['ACList' + str(I)][J].available_time_today
                            country_training_flying_sum += AC.ACDict['ACList' + str(I)][J].flying_time_today
                            country_training_BAR_sum += AC.ACDict['ACList' + str(I)][J].BAR_time_today
                            country_training_BAP_sum += AC.ACDict['ACList' + str(I)][J].BAP_time_today
                            country_training_BBR_sum += AC.ACDict['ACList' + str(I)][J].BBR_time_today
                        elif AC.ACDict['ACList' + str(I)][J].mission_type == "combat":
                            country_combat_available_sum += AC.ACDict['ACList' + str(I)][J].available_time_today
                            country_combat_flying_sum += AC.ACDict['ACList' + str(I)][J].flying_time_today
                            country_combat_BAR_sum += AC.ACDict['ACList' + str(I)][J].BAR_time_today
                            country_combat_BAP_sum += AC.ACDict['ACList' + str(I)][J].BAP_time_today
                    overall_AO=0
                    training_AO=0
                    combat_AO=0
                    overall_AO=(float(country_available_sum+country_flying_sum))/(float(country_available_sum+country_flying_sum+country_BAR_sum+country_BAP_sum+country_BBR_sum))
                    training_AO=(float(country_training_available_sum+country_training_flying_sum))/(float(country_training_available_sum+country_training_flying_sum+country_training_BAR_sum+country_training_BAP_sum+country_training_BBR_sum))
                    if (country_combat_available_sum+country_combat_flying_sum+country_combat_BAR_sum+country_combat_BAP_sum+country_combat_BBR_sum) == 0:
                        combat_AO=0
                    else:    
                        combat_AO=(float(country_combat_available_sum+country_combat_flying_sum))/(float(country_combat_available_sum+country_combat_flying_sum+country_combat_BAR_sum+country_combat_BAP_sum+country_combat_BBR_sum))
                    ao_countrylevel_string = ao_countrylevel_string + ',' + str(country_available_sum) + ',' + str(country_flying_sum) + ',' + str(country_BAR_sum) + ',' + str(country_BAP_sum) + ',' + str(country_BBR_sum) + ',' + str(overall_AO)
                    ao_countrylevel_string = ao_countrylevel_string + ',' + str(country_training_available_sum) + ',' + str(country_training_flying_sum) + ',' + str(country_training_BAR_sum) + ',' + str(country_training_BAP_sum) + ',' + str(country_training_BBR_sum) + ',' + str(training_AO)
                    ao_countrylevel_string = ao_countrylevel_string + ',' + str(country_combat_available_sum) + ',' + str(country_combat_flying_sum) + ',' + str(country_combat_BAR_sum) + ',' + str(country_combat_BAP_sum) + ',' + str(country_combat_BBR_sum) + ',' + str(combat_AO)
                    ro_countrylevel_string = ro_countrylevel_string + ',' + str(SortieGen.SortieDict['SortieList' + str(I)][0].training_required) + ',' + str(SortieGen.SortieDict['SortieList' + str(I)][0].training_required - SortieGen.SortieDict['SortieList' + str(I)][0].training_sortie_count) + ',' + str(SortieGen.SortieDict['SortieList' + str(I)][0].training_sortie_flown) 
                    ro_countrylevel_string = ro_countrylevel_string + ',' + str(SortieGen.SortieDict['SortieList' + str(I)][0].combat_required) + ',' + str(SortieGen.SortieDict['SortieList' + str(I)][0].combat_required - SortieGen.SortieDict['SortieList' + str(I)][0].combat_sortie_count) + ',' + str(SortieGen.SortieDict['SortieList' + str(I)][0].combat_sortie_flown)
                    ro_countrylevel_string = ro_countrylevel_string + ',' + str(len(AC.ACDict['ACcombatAvailable' + str(I)])) + ',' + str(len(AC.ACDict['ACtrainingAvailable' + str(I)])) 
                inputs.ao_countrylevel_file.write(ao_countrylevel_string+'\n')
                inputs.ro_countrylevel_file.write(ro_countrylevel_string+'\n')     
                for I in range(len(inputs.num_ac)):
                    SortieGen.SortieDict['SortieList' + str(I)][0].training_sortie_flown = 0
                    SortieGen.SortieDict['SortieList' + str(I)][0].combat_sortie_flown = 0
                    for J in range(inputs.num_ac[I]):
                        AC.ACDict['ACList' + str(I)][J].available_time_today = 0
                        AC.ACDict['ACList' + str(I)][J].flying_time_today = 0
                        AC.ACDict['ACList' + str(I)][J].BAR_time_today = 0
                        AC.ACDict['ACList' + str(I)][J].BAP_time_today = 0
                        AC.ACDict['ACList' + str(I)][J].BBR_time_today = 0                                
            yield hold, self, 24

def main():
    initialize()
    ac_counter = [0, 0, 0, 0, 0]
    for I in range(sum(inputs.num_ac)):
        for J in range(len(inputs.num_ac)):
            if ac_counter[J] < inputs.num_ac[J]:
                A = AC(J)
                activate(A,A.Run())
                ac_counter[J] += 1
    Q = Queue()
    activate(Q,Q.Run())
    P = Parts()
    activate(P,P.Run())
    for I in range(len(inputs.num_ac)):
        Sortie = SortieGen(I)
        activate(Sortie,Sortie.Run())
    inventoryDict={}
    inventoryCount=0
    for I in range(len(inputs.num_ac)):
        for J in range(inputs.num_ac[I]):
            for K in range(100):
                inventoryDict[str(inventoryCount)]=inventory0(['equip_ac',(J+sum(inputs.num_ac[0:I]))],1)
                inventoryCount+=1
                inventoryDict[str(inventoryCount)]=inventory1(['equip_ac',(J+sum(inputs.num_ac[0:I]))],2)
                inventoryCount+=1
    
    localinventory=[[13,78,148,598,1376],
                    [3,21,32,176,375]]     
    for J in range(len(inputs.num_ac)):
        for I in range(localinventory[0][J]):
            inventoryDict[str(inventoryCount)]=inventory0(['training_local',J], 1)
            inventoryCount+=1
        for I in range(localinventory[1][J]):
            inventoryDict[str(inventoryCount)]=inventory1(['training_local',J], 2)
            inventoryCount+=1
            
    combatlocalinventory=[879,242]     
    for I in range(combatlocalinventory[0]):
        inventoryDict[str(inventoryCount)]=inventory0(['combat_local'], 1)
        inventoryCount+=1
    for I in range(combatlocalinventory[1]):
        inventoryDict[str(inventoryCount)]=inventory1(['combat_local'], 2)
        inventoryCount+=1
    
    poolinventory= [[182,1489,2751],[48,107,750]]         
    for J in range(3):
        for I in range(poolinventory[0][J]):
            inventoryDict[str(inventoryCount)]=inventory0(['pool',J], 1)
            inventoryCount+=1
        for I in range(poolinventory[1][J]):
            inventoryDict[str(inventoryCount)]=inventory1(['pool',J], 2)
            inventoryCount+=1
           
    D = Daily()
    activate(D,D.Run())
    MaxSimtime = 23856.
    simulate(until=MaxSimtime)

if __name__ == '__main__': main()
