#!/usr/bin/env python3

import math


def Locate_Asteroid_Positions(Data):
    height = range(len(Data))
    locations = []

    for y_pos in height:
        width = range(len(Data[y_pos]))
        for x_pos in width:
            if Data[y_pos][x_pos] == '#':
                locations.append((x_pos,y_pos))
    
    return locations

def Add_Quotient(Asteroid_Coord, New_Asteroid_Coord, Set):

    x_diff = Asteroid_Coord[0]-New_Asteroid_Coord[0]
    y_diff = Asteroid_Coord[1]-New_Asteroid_Coord[1]

    greatest_common_divisor = math.gcd(x_diff,y_diff)

    x_diff = x_diff / greatest_common_divisor
    y_diff = y_diff / greatest_common_divisor

    coordinates = "({},{})".format(x_diff,y_diff)

    if coordinates not in Set:
        Set.add(coordinates)

    return Set

def Add_Vertical(Asteroid_Coord, New_Asteroid_Coord, vertical_set):
    if New_Asteroid_Coord[1] > Asteroid_Coord[1]:
        x = 1
    else:
        x = -1
    
    if x not in vertical_set:
        vertical_set.add(x)

    return vertical_set

def If_Reachable(Asteroid_Coord, New_Asteroid_Coord, left_set, right_set):

    if Asteroid_Coord[0] > New_Asteroid_Coord[0]:
        return Add_Quotient(Asteroid_Coord, New_Asteroid_Coord, left_set), right_set
    else:
        return left_set, Add_Quotient(Asteroid_Coord, New_Asteroid_Coord, right_set)


def Number_Of_Reachable_Asteroids(Location_Map, Position):
    left_positions = set()
    right_positions = set()
    vertical_positions = set()

    for asteroid in Location_Map:
        if asteroid == Position:
            pass
        elif asteroid[0] == Position[0]:
            vertical_positions = Add_Vertical(Position, asteroid, vertical_positions)

        else:
            left_positions, right_positions = If_Reachable(Position, asteroid, left_positions, right_positions)
    
    reachable_number = len(left_positions) + len(right_positions) + len(vertical_positions)

    return reachable_number



def Program(Data):

    #Part 1
    asteroid_positions = Locate_Asteroid_Positions(Data)
    max_reachable = 0

    for asteroid in asteroid_positions:
        asteroid_reachable = Number_Of_Reachable_Asteroids(asteroid_positions, asteroid)

        if asteroid_reachable > max_reachable:
            max_reachable = asteroid_reachable
            asteroid_position = asteroid

    print("Answer, Part 1: The maximum amount of reachable asteroids is {}, from asteroid at position {}.".format(max_reachable,asteroid_position))



if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [x.rstrip() for x in f.readlines()]

    Program(Data)
