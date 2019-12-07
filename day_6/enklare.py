#!/usr/bin/env python3

def Program_1(Orbit_Map): 
    count = 0
    for orbit in Orbit_Map.keys():
        planet = orbit
        while planet in Orbit_Map:
            count += 1
            planet = Orbit_Map[planet] 
    print("Part 1, Answer: {}".format(count))

def Program_2(Orbit_Map, Planet_1, Planet_2):
    First_Orbit_List = []
    Second_Orbit_List = []
    first = Planet_1
    second = Planet_2

    while first in Orbit_Map.keys():
        first = Orbit_Map[first]
        First_Orbit_List.append(first)  
    while second in Orbit_Map.keys():
        second = Orbit_Map[second]
        Second_Orbit_List.append(second)
    
    First_Orbit_List = First_Orbit_List[::-1]
    Second_Orbit_List = Second_Orbit_List[::-1]
    while First_Orbit_List[0] == Second_Orbit_List[0]:
        First_Orbit_List = First_Orbit_List[1:]
        Second_Orbit_List = Second_Orbit_List[1:]
    print("Part 2, Answer: {}".format(len(First_Orbit_List)+len(Second_Orbit_List)))

if __name__ == '__main__':
    f = open("data.txt", "r")
    Orbit_Map = dict()
    for line in f.readlines():
        planet, orbitting_planet = line.rstrip().split(')')
        Orbit_Map[orbitting_planet] = planet
    Program_1(Orbit_Map)
    Program_2(Orbit_Map, 'YOU', 'SAN')