#!/usr/bin/env python3

import math
import queue

def Locate_Asteroid_Positions(Data):

    height = range(len(Data))
    locations = []

    for y_pos in height:
        width = range(len(Data[y_pos]))
        for x_pos in width:
            if Data[y_pos][x_pos] == '#':
                locations.append((x_pos,y_pos))
    return locations

def Add_If_Reachable(Asteroid_Coord, New_Asteroid_Coord, Set):

    x_diff = Asteroid_Coord[0] - New_Asteroid_Coord[0]
    y_diff = Asteroid_Coord[1] - New_Asteroid_Coord[1]
    greatest_common_divisor = abs(math.gcd(x_diff,y_diff))
    x_diff = x_diff / greatest_common_divisor
    y_diff = y_diff / greatest_common_divisor
    coordinates = "({},{})".format(x_diff,y_diff)

    if coordinates not in Set:
        Set.add(coordinates)
    return Set

def Number_Of_Reachable_Asteroids(Location_Map, Position):

    reachable_positions = set()

    for asteroid in Location_Map:
        if asteroid != Position:
            reachable_positions = Add_If_Reachable(Position, asteroid, reachable_positions)
    return len(reachable_positions)

def Get_All_Relative_Asteroid_Positions(Location_Map, Asteroid_Coord):

    Relative_Distances = []

    for asteroid in Location_Map:
        if asteroid != Asteroid_Coord:
            Relative_Distances.append((asteroid[0]-Asteroid_Coord[0], asteroid[1]-Asteroid_Coord[1]))
    return Relative_Distances

def Map_Coordinates_To_Angles(Asteroid_Coord, Dict):

    X_coord = Asteroid_Coord[0]
    Y_coord = - Asteroid_Coord[1] # Compensation for the fact that the Y-axis is inverted.
    distance = math.hypot(X_coord,Y_coord)
    angle = math.atan2(X_coord,Y_coord) 

    if angle < 0:
        angle += 2*math.pi
    
    if angle in Dict.keys():
        Dict[angle][distance] = Asteroid_Coord
    else:
        Dict[angle] = {distance: Asteroid_Coord}
    return Dict


def Destroy_Next(Dict, Angle):

    Candidates = Dict[Angle]
    Closest_dist = min(Candidates.keys())
    Coordinate = Candidates[Closest_dist]
    Dict[Angle].pop(Closest_dist)
    return Coordinate, Dict


def Destroy_Many(Dict, queue, n):

    counter = 0

    while counter < n:
        next_angle = queue.get()
        if len(Dict[next_angle]) > 0:
            queue.put(next_angle)
            Destroyed_Planet, Dict = Destroy_Next(Dict, next_angle)
            counter += 1
        if queue.empty():
            break
    return Destroyed_Planet


def Program(Data):

    #Part 1

    asteroid_positions = Locate_Asteroid_Positions(Data)
    max_reachable = 0

    for asteroid in asteroid_positions:
        asteroid_reachable = Number_Of_Reachable_Asteroids(asteroid_positions, asteroid)
        if asteroid_reachable > max_reachable:
            max_reachable = asteroid_reachable
            asteroid_position = asteroid
    print("Answer, Part 1: The maximum amount of reachable asteroids is {}, from the asteroid at position {}.".format(max_reachable,asteroid_position))



    #Part 2

    relative_distances = Get_All_Relative_Asteroid_Positions(asteroid_positions, asteroid_position)
    mapping_angles = {}

    for asteroid in relative_distances:
        mapping_angles = Map_Coordinates_To_Angles(asteroid, mapping_angles)
    angles_sorted = sorted([x for x in mapping_angles.keys()])
    q = queue.Queue()

    for angle in angles_sorted:
        q.put(angle)

    relative_coordinates = Destroy_Many(mapping_angles, q, 200)
    real_position = (relative_coordinates[0] + asteroid_position[0], relative_coordinates[1] + asteroid_position[1])
    ans = 100 * (real_position[0]) + real_position[1]
    print("Answer, Part 2: {}".format(ans))


if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [x.rstrip() for x in f.readlines()]

    Program(Data.copy())
