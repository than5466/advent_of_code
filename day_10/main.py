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

def Add_Quotient(Position, Add_Position, Set):

    x_diff = Position[0]-Add_Position[0]
    y_diff = Position[1]-Add_Position[1]

    greatest_common_divisor = math.gcd(x_diff,y_diff)

    x_diff = x_diff / greatest_common_divisor
    y_diff = y_diff / greatest_common_divisor

    coordinates = "({},{})".format(x_diff,y_diff)

    if coordinates not in Set:
        Set.add(coordinates)

    return Set


def Add_Correct(Position, Add_Position, left_set, right_set):

    if Position[0] > Add_Position[0]:
        return Add_Quotient(Position, Add_Position, left_set), right_set
    else:
        return left_set, Add_Quotient(Position, Add_Position, right_set)

def Add_Vertical(Position, Add_Position, vertical_set):
    if Add_Position[1] > Position[1]:
        x = 1
    else:
        x = -1
    
    if x not in vertical_set:
        vertical_set.add(x)

    return vertical_set


def Number_Of_Reachable_Asteroids(Location_Map, Position):
    left_positions = set()
    right_positions = set()
    vertical_positions = set()

    for each in Location_Map:
        if each == Position:
            pass
        elif each[0] == Position[0]:
            vertical_positions = Add_Vertical(Position, each, vertical_positions)

        else:
            left_positions, right_positions = Add_Correct(Position, each, left_positions, right_positions)
    
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
    #f = open("test_data.txt", "r")
    #f = open("test_data_2.txt", "r")
    Data = [x.rstrip() for x in f.readlines()]

    Program(Data)
