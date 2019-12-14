#!/usr/bin/env python3

def relative_cost(dict):
    Known_Costs = {'1 ORE':1}
    Unknown_Costs = set()
    for k,v in dict.items():
        for Ore_Number in k.split(", "):
            Ore = Ore_Number.split(" ")[1]
            if Ore not in Known_Costs.keys():
                Unknown_Costs.add(Ore)
        for Ore_Number in v.split(", "):
            Ore = Ore_Number.split(" ")[1]
            if Ore not in Known_Costs.keys():
                Unknown_Costs.add(Ore)
    return Known_Costs, Unknown_Costs

def Program(dict):
    Known, Unknown = relative_cost(dict)

if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = {x.rstrip().split(" => ")[0]:x.rstrip().split(" => ")[1] for x in f.readlines()}
    #print(Data)