#!/usr/bin/env python3

class Node(object):
    def __init__(self, data, depth):
        self.data = data
        self.children = []
        self.depth = depth

    def addChild(self, child):
        self.children.append(child)

    def getData(self):
        return self.data
    
    def getChildren(self):
        return self.children

    def getDepth(self):
        return self.depth


def Add_Orbit(Map, Orbit, All_Orbitting_Planets):
    planet, orbitting_planet = Orbit.rstrip().split(')')
    
    if planet in Orbit_Map.keys():
        Orbit_Map[planet].append(orbitting_planet)
    else:
        Orbit_Map[planet] = [orbitting_planet]
    All_Orbitting_Planets.add(orbitting_planet)
    return Orbit_Map, All_Orbitting_Planets


def Recursive_Descent(planet_node, orbit_map):
    planet = planet_node.getData()
    depth = planet_node.getDepth()

    if planet in orbit_map.keys():
        orbits = orbit_map[planet]

        for orbit in orbits:
            planet_node.addChild(Recursive_Descent(Node(orbit, depth+1), orbit_map))
        return planet_node

    else:
        return Node(planet, depth)


def Tree(orbit_map, all_orbitting_planets):
    All_orbits = []

    for planet in orbit_map.keys():
        if planet in all_orbitting_planets:
            pass
        else:
            Planet_Node = Node(planet,0)
            All_orbits.append(Recursive_Descent(Planet_Node, orbit_map))

    return All_orbits

def Count_Indirect_Orbits(Node):
    depth = Node.getDepth()

    if depth < 2:
        depth = 0
    else:
        depth = depth - 1

    if Node.getChildren():
        total_Depth = depth
        for child in Node.getChildren():
            total_Depth += Count_Indirect_Orbits(child)

        return total_Depth

    else:
        return depth


def Program_1(orbit_map, tree):
    direct_orbits = 0

    for planet in orbit_map.keys():
        direct_orbits += len(orbit_map[planet])
    indirect_orbits = 0

    for node in tree:
        indirect_orbits += Count_Indirect_Orbits(node)

    print("First Part, Number of Orbits is {}".format(indirect_orbits+direct_orbits))


def Orbit_List(Orbit_Map, Planet):
    lst = []
    current_planet = Planet
    lst.append(Planet)

    while True:
        checker = current_planet
        for key, value in Orbit_Map.items():
            if current_planet in value:
                current_planet = key
                lst.append(current_planet)
                break
        
        if checker == current_planet:

            return lst[::-1]

    
def Program_2(Orbit_Map, Planet_1, Planet_2):

    Planet_1_Orbits = Orbit_List(Orbit_Map, Planet_1)
    Planet_2_Orbits = Orbit_List(Orbit_Map, Planet_2)

    while Planet_1_Orbits[0] == Planet_2_Orbits[0]:
        Planet_1_Orbits = Planet_1_Orbits[1:]
        Planet_2_Orbits = Planet_2_Orbits[1:]
    
    Planet_1_Orbits = Planet_1_Orbits[1:]
    Planet_2_Orbits = Planet_2_Orbits[1:]
    
    print("Part 2, Answer: {}".format(len(Planet_1_Orbits) + len(Planet_2_Orbits)))
    

if __name__ == '__main__':
    f = open("data.txt", "r")
    Orbit_Map = dict()
    Orbitting_Planets = set()

    for line in f.readlines():
        Orbit_Map, Orbitting_Planets = Add_Orbit(Orbit_Map, line, Orbitting_Planets)
    
    Galaxy_Tree = Tree(Orbit_Map, Orbitting_Planets)
    Program_1(Orbit_Map, Galaxy_Tree)

    Program_2(Orbit_Map, 'YOU', 'SAN')
