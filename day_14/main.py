#!/usr/bin/env python3

import math

import copy

def Dependants(Data):
    dependants = {}
    while True:
        copy = dependants.copy()
        for k,v in Data.items():
            keys = k.split(', ')
            keys = [x.split(' ')[1] for x in keys]
            value = v.split(' ')[1]
            if keys[0] == 'ORE':
                dependants[value] = set()
            else:
                check = True
                for key in keys:
                    if key not in dependants.keys():
                        check = False
                        break
                if check:
                    dependants[value] = set()
                    for key in keys:
                        dependants[value].add(key)
                        for material in dependants[key]:
                            dependants[value].add(material)
                            

        if copy == dependants:
            break

    for i in dependants.keys():
        for j in dependants[i]:
            if i == j:
                print('här är felet')
    return dependants

def None_Dependant(dependant, dependant_dict, materials):

    for key, values in dependant_dict.items():
        if dependant in values and key in materials:
            return False
    
    return True


def Update_Materials(Fuel_Costs, New_Values, Old_Value, Amount):
    Fuel_Costs.remove(Old_Value)
    multiplier = int(Old_Value.split(' ')[0])
    divisor = int(Amount.split(' ')[0])

    for index in range(len(New_Values)):
        New_Values[index] = '{} {}'.format(math.ceil(multiplier/divisor)*int(New_Values[index].split(' ')[0]), New_Values[index].split(' ')[1])
    
    Fuel_Costs = Update_Duplicates(Fuel_Costs+New_Values)
    return Fuel_Costs

def Update_Duplicates(Fuel_Costs):
    summation = {}

    for each_cost in Fuel_Costs:
        Amount, Material = each_cost.split(' ')
        Amount = int(Amount)
        if Material in summation.keys():
            summation[Material] += Amount
        else:
            summation[Material] = Amount
    
    Fuel_Costs = []
    for key,value in summation.items():
        Fuel_Costs.append('{} {}'.format(value,key))
    
    return Fuel_Costs

def Calculate_Cost(Fuel_Costs, Known_Costs):

    summed_costs = 0
    Fuel_Costs = Update_Duplicates(Fuel_Costs)
    for each_cost in Fuel_Costs:
        [Material_Amount,Material_Type] = each_cost.split(' ')
        Material_Amount = int(Material_Amount)
        for k,v in Known_Costs.items():
            if Material_Type == v.split(' ')[1]:
                divisor = int(v.split(' ')[0])
                multiplier = int(k.split(' ')[0])
                summed_costs += math.ceil(Material_Amount/divisor)*multiplier
                break
    return summed_costs


def Known_Cost(Data):
    Known_Costs = {}
    for k,v in Data.items():
        if 'ORE' in k:
            Known_Costs[k] = v
    return Known_Costs

def Fuel_Cost(Data):
    Fuel_Costs = {}
    for k,v in Data.items():
        if 'FUEL' in v:
            Fuel_Costs[v] = k.split(', ')
    return Fuel_Costs

def Recursive_Descent(Data, Known_Costs, Fuel_Cost, Basic_Materials, dependants):
    materials = set()

    for material in Fuel_Cost:
        materials.add(material.split(' ')[1])
    
    if materials.issubset(Basic_Materials):
        return Calculate_Cost(Fuel_Cost, Known_Costs)

    possible_routes = []
    
    for material in Fuel_Cost:
        if material.split(' ')[1] not in Basic_Materials and None_Dependant(material.split(' ')[1], dependants, materials):
            for k,v in Data.items():
                if v.split(' ')[1] == material.split(' ')[1]:
                    elements = k.split(', ')
                    possible_routes.append(Recursive_Descent(Data, Known_Costs, Update_Materials(Fuel_Cost.copy(),elements,material,v), Basic_Materials, dependants))
            break
    return min(possible_routes)


def Program(Data):

    #Part 1

    Known_Ore_Costs = Known_Cost(Data)
    Fuel_Costs = Fuel_Cost(Data)
    Basic_Materials = set()
    for key in Known_Ore_Costs.values():
        Basic_Materials.add(key.split(' ')[1])

    candidates = []
    dependants = Dependants(Data)

    for v in Fuel_Costs.values():
        candidates.append(Recursive_Descent(Data, Known_Ore_Costs, v, Basic_Materials, dependants))
    ans = min(candidates)
    print('Answer, Part 1: {}'.format(ans))

    # Part 2

    candidates = []

    GOAL = pow(10,12)
    START = 2000000
    END = 3000000

    while True:

        Copy = copy.deepcopy(Fuel_Costs)

        middle_point = (START + END) // 2 

        for v in Copy.values():
            for i in range(len(v)):
                v[i] = '{} {}'.format(middle_point * int(v[i].split(' ')[0]), v[i].split(' ')[1])
            candidate = Recursive_Descent(Data, Known_Ore_Costs, v, Basic_Materials, dependants)
        
        if candidate < GOAL:
            START = middle_point
        else:
            END = middle_point

        if END - START == 1:
            if END == middle_point:
                ans = START
            else:
                ans = END
            break
    print('Answer, Part 2: {}'.format(ans))

if __name__ == '__main__':
    #f = open("test.txt", "r")
    f = open("data.txt", "r")
    Data = {x.rstrip().split(" => ")[0]:x.rstrip().split(" => ")[1] for x in f.readlines()}
    Program(Data.copy())
