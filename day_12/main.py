#!/usr/bin/env python3

from coordinates import Coordinate
import math

def lcm(a, b): #least common multiple
    return abs(a*b) // math.gcd(a, b)

def lcm3(a,b,c):
    return lcm(lcm(a,b),c)

def Data_Processing(In_Data):
    Processed_Data = []

    for row in In_Data:
        Split_Coordinates = row[1:-1].split(', ')
        x_coord = int(Split_Coordinates[0][2:])
        y_coord = int(Split_Coordinates[1][2:])
        z_coord = int(Split_Coordinates[2][2:])
        coord = Coordinate(x=x_coord,y=y_coord,z=z_coord,x_velocity=0,y_velocity=0,z_velocity=0)
        Processed_Data.append(coord)
    
    return Processed_Data

def Change_Velocity(Coord_1, Coord_2):

    if Coord_1 > Coord_2:
        return -1
    elif Coord_1 < Coord_2:
        return 1
    else:
        return 0

def Update_Velocity(Moons):

    for coord in Moons:
        for row in Moons:
            coord.x_velocity += Change_Velocity(coord.x,row.x)
            coord.y_velocity += Change_Velocity(coord.y,row.y)
            coord.z_velocity += Change_Velocity(coord.z,row.z)
    
    return Moons

def Update_Position(Moons):

    for Moon in Moons:
        Moon.x += Moon.x_velocity
        Moon.y += Moon.y_velocity
        Moon.z += Moon.z_velocity
    return Moons

def Update(Moons):
    return Update_Position(Update_Velocity(Moons))

def Potential_Energy(Moon):
    return abs(Moon.x) + abs(Moon.y) + abs(Moon.z)

def Kinetic_Energy(Moon):
    return abs(Moon.x_velocity) + abs(Moon.y_velocity) + abs(Moon.z_velocity)

def Find_Part_Match(Moons, coord):
    time_duration = 0
    Moon_Info = Moons.copy()
    Previous_Moon_Positions = set()

    if coord == 'x':
        while True:
            moon_positions = ['({},{})'.format(moon.x,moon.x_velocity) for moon in Moon_Info]
            moon_positions = ",".join(moon_positions)
            if moon_positions in Previous_Moon_Positions:
                break
            else:
                Previous_Moon_Positions.add(moon_positions)
            Moon_Info = Update(Moon_Info)
            time_duration += 1
    elif coord == 'y':
        while True:
            moon_positions = ['({},{})'.format(moon.y,moon.y_velocity) for moon in Moon_Info]
            moon_positions = ",".join(moon_positions)
            if moon_positions in Previous_Moon_Positions:
                break
            else:
                Previous_Moon_Positions.add(moon_positions)
            Moon_Info = Update(Moon_Info)
            time_duration += 1
    elif coord == 'z':
        while True:
            moon_positions = ['({},{})'.format(moon.z,moon.z_velocity) for moon in Moon_Info]
            moon_positions = ",".join(moon_positions)
            if moon_positions in Previous_Moon_Positions:
                break
            else:
                Previous_Moon_Positions.add(moon_positions)
            Moon_Info = Update(Moon_Info)
            time_duration += 1
    
    return time_duration

def Program_1(Data, time_left):
    Moon_Info = Data
    Total_Energy = 0

    while 0 < time_left:
        Moon_Info = Update(Moon_Info)
        time_left -= 1
    
    for Moon in Moon_Info:
        Total_Energy += Kinetic_Energy(Moon)*Potential_Energy(Moon)
    
    return Total_Energy

def Part_1(Data):
    Moon_Info = Data_Processing(Data.copy())
    energy = Program_1(Moon_Info, 1000)

    print("Answer, Part 1: {}".format(energy))

def Program_2(Data):

    Moon_Info = Data_Processing(Data.copy())
    x_order = Find_Part_Match(Moon_Info,'x')
    y_order = Find_Part_Match(Moon_Info,'y')
    z_order = Find_Part_Match(Moon_Info,'z')
    return lcm3(x_order,y_order,z_order)


def Part_2(Data):
    
    time = Program_2(Data)

    print("Answer, Part 2: {}".format(time))

if __name__ == '__main__':
    f = open("data.txt", "r")

    Raw_Data = [x.rstrip() for x in f.readlines()]
    Part_1(Raw_Data.copy())
    Part_2(Raw_Data.copy())