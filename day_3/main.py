#!/usr/bin/env python3

import sys

def Calculate_Node(Direction,Len,Prev):

    X_coord = Prev[0]
    Y_coord = Prev[1]

    if Direction in 'UDLR':
        if Direction == 'U':
            return [X_coord, Y_coord + Len]
        elif Direction == 'D':
            return [X_coord, Y_coord - Len]
        elif Direction == 'L':
            return [X_coord - Len, Y_coord]
        elif Direction == 'R':
            return [X_coord + Len, Y_coord]

    else:
        sys.exit("Something is wrong.")

def Add_Road(Start_Node, End_Node, road):

    X_coord_diff = End_Node[0] - Start_Node[0]
    Y_coord_diff = End_Node[1] - Start_Node[1]

    if X_coord_diff > 0:
        for i in range(1, X_coord_diff+1):
            road_segment = str(Start_Node[0]+i) + ',' + str(Start_Node[1])
            road[road_segment] = 1
    
    elif X_coord_diff < 0:
        for i in range(X_coord_diff, 0):
            road_segment = str(Start_Node[0]+i) + ',' + str(Start_Node[1])
            road[road_segment] = 1

    elif Y_coord_diff > 0:
        for i in range(1, Y_coord_diff+1):
            road_segment = str(Start_Node[0]) + ',' + str(Start_Node[1]+i)
            road[road_segment] = 1
    
    elif Y_coord_diff < 0:
        for i in range(Y_coord_diff, 0):
            road_segment = str(Start_Node[0]) + ',' + str(Start_Node[1]+i)
            road[road_segment] = 1
    
    else:
        sys.exit("Something is wrong.")

    return road


def Found_Intersection(Start_Node, End_Node, Goal_Node):

    if Start_Node[0] == Goal_Node[0] and End_Node[0] == Goal_Node[0]:
        if Start_Node[1] > Goal_Node[1] and End_Node[1] < Goal_Node[1]:
            return True
        elif Start_Node[1] < Goal_Node[1] and End_Node[1] > Goal_Node[1]:
            return True

    elif Start_Node[1] == Goal_Node[1] and End_Node[1] == Goal_Node[1]:
        if Start_Node[0] > Goal_Node[0] and End_Node[0] < Goal_Node[0]:
            return True
        elif Start_Node[0] < Goal_Node[0] and End_Node[0] > Goal_Node[0]:
            return True

    else:
        return False

def Evaluate(Node,var):

    Direction = var[0]
    Length = int(var[1:])
    
    return Calculate_Node(Direction,Length,Node)

def Intersecting_Distances(dict1,dict2):

    List_of_Distances = []

    for key in dict1.keys():
        if key in dict2.keys():
            Coordinates = key.split(',')
            X_coord = int(Coordinates[0])
            Y_coord = int(Coordinates[1])
            List_of_Distances.append([X_coord,Y_coord])

    return List_of_Distances

def Min_Distance(dict1, dict2):

    coordinates = Intersecting_Distances(dict1,dict2)
    distances = []

    for i in coordinates:
        distances.append(abs(i[0])+abs(i[1]))

    return min(distances)

def Calculation(Start_Node, End_Node):

    return abs(Start_Node[0]-End_Node[0])+abs(Start_Node[1]-End_Node[1])


def Calculate_Distance(Data, intersection):

    Coordinates = intersection
    Data_Distance = 0
    Current_Edge = [0,0]

    for i in Data:
        Next_Edge = Evaluate(Current_Edge,i)
        if Found_Intersection(Current_Edge, Next_Edge, Coordinates):
            Data_Distance += Calculation(Current_Edge,Coordinates)
            break
        else:
            Data_Distance += Calculation(Current_Edge, Next_Edge)
            Current_Edge = Next_Edge 

    return Data_Distance

def Part_1_Go(Start, Path):

    Visited = {}
    Distances = []
    
    for i in Path:
        if Distances == []:
            Next_Edge = Evaluate(Start,i)
        else:
            Next_Edge = Evaluate(Distances[-1],i)
        Distances.append(Next_Edge)
        if len(Distances) == 1:
            Visited = Add_Road([0,0],Next_Edge, Visited)
        else:
            Visited = Add_Road(Distances[-2],Distances[-1],Visited)

    return Visited

def Part_2_Go(Data_1,Data_2,Dict1,Dict2):

    Intersections = Intersecting_Distances(Dict1,Dict2)
    Distances = []

    for i in Intersections:
        distance = Calculate_Distance(Data_1,i) + Calculate_Distance(Data_2,i)
        Distances.append(distance)

    return min(Distances)



if __name__ == '__main__':

    f = open("input.txt", "r")
    Original_Data = []
    for line in f.readlines():
        Original_Data.append([x for x in line.split(",")])
    
    Central_Port = [0,0]
    First_Data = Original_Data[0]
    Second_Data = Original_Data[1]
    First = Part_1_Go(Central_Port, First_Data)
    Second = Part_1_Go(Central_Port, Second_Data)
    ans = Min_Distance(First,Second)

    print("First question, answer: {}".format(ans))

    ans = Part_2_Go(First_Data,Second_Data,First,Second)

    print("Second question, answer: {}".format(ans))