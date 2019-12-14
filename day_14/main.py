#!/usr/bin/env python3

import math

def Calculate_Cost(Fuel_Costs, Known_Costs):

    summed_costs = 0

    for each_cost in Fuel_Costs:
        [Material_Amount,Material_Type] = each_cost.split(' ')
        Material_Amount = int(Material_Amount)
        for k,v in Known_Costs.items():
            if Material_Type in k:
                divisor = int(k.split(' ')[0])
                multiplier = int(v.split(' ')[0])
                summed_costs += math.ceil(Material_Amount/divisor)*multiplier
                break
    print(summed_costs)



def Known_Cost(Data):
    Known_Costs = {}
    for k,v in Data.items():
        if 'ORE' in k:
            Known_Costs[v] = k
    return Known_Costs

def Fuel_Cost(Data):
    Fuel_Costs = {}
    for k,v in Data.items():
        if 'FUEL' in v:
            Fuel_Costs[k] = v
    return Fuel_Costs

def Recursive_Descent(Data, Known_Costs, Fuel_Cost):
    pass


def Program(Data):
    Known_Ore_Costs = Known_Cost(Data)
    Fuel_Costs = Fuel_Cost(Data)
    Basic_Materials = set()
    for key in Known_Ore_Costs.keys():
        Basic_Materials.add(key.split(' ')[1])
    print(Known_Ore_Costs, Fuel_Costs, Basic_Materials)
    Calculate_Cost(['7 TLJL'], Known_Ore_Costs)

if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = {x.rstrip().split(" => ")[0]:x.rstrip().split(" => ")[1] for x in f.readlines()}
    #print(Data)
    Program(Data)