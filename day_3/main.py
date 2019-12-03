#!/usr/bin/env python3


def Calculate_Next_Node(Dir,Len,Prev, Visited):
    X_coord = Prev[0]
    Y_coord = Prev[1]

    if Dir in 'UDLR':
        if Dir == 'U':

            for i in range(1,Len+1):

                hash = str(X_coord) + ',' + str(Y_coord + i)
                
                Visited[hash] = 1
            
            return [X_coord, Y_coord + Len], Visited

        elif Dir == 'D':

            for i in range(1,Len+1):

                hash = str(X_coord) + ',' + str(Y_coord - i)
                
                Visited[hash] = 1

            return [X_coord, Y_coord - Len], Visited

        elif Dir == 'L':

            for i in range(1,Len+1):

                hash = str(X_coord - i) + ',' + str(Y_coord)
                
                Visited[hash] = 1

            return [X_coord - Len, Y_coord], Visited
        
        elif Dir == 'R':

            for i in range(1,Len+1):
                
                hash = str(X_coord + i) + ',' + str(Y_coord)

                Visited[hash] = 1

            return [X_coord + Len, Y_coord], Visited

    else:
        print("Something is wrong.")

def Between_points(Dir,Len,Prev, goal):
    X_coord = Prev[0]
    Y_coord = Prev[1]

    if Dir in 'UDLR':
        if Dir == 'U':

            if goal[0] == X_coord and (Y_coord <= goal[1] and goal[1]<= Y_coord + Len):
                return True, abs(goal[1] - Y_coord)
            
            else:
                return False, Len

        elif Dir == 'D':

            if goal[0] == X_coord and (Y_coord >= goal[1] and goal[1]>= Y_coord - Len):
                return True, abs(Y_coord - goal[1])

            else:
                return False, Len

        elif Dir == 'L':

            if goal[1] == Y_coord and (X_coord  >= goal[0] and goal[0]>= X_coord  - Len):
                return True, abs(goal[0] - X_coord)
            
            else:
                return False, Len
        
        elif Dir == 'R':

            if goal[1] == Y_coord and (X_coord  <= goal[0] and goal[0]<= X_coord  + Len):
                return True, abs(X_coord - goal[0])
            
            else:
                return False, Len

    else:
        print("Something is wrong.")

def Evaluate(lst,var,visitedroads):

    Direction = var[0]
    Length = int(var[1:])
    if lst == []:
        Previous_Point = [0,0]
    else:
        Previous_Point = lst[-1]
    
    return Calculate_Next_Node(Direction,Length,Previous_Point, visitedroads)

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


def Part_1_Go(Start, Path, Visited):

    next_point = Start

    Distance_From_Start_Point = []

    

    for i in Path:
        next_point, Visited = Evaluate(Distance_From_Start_Point,i, Visited)
        Distance_From_Start_Point.append(next_point)

    return Visited


def Calculate_Distance(Data_1,Data_2, intersection):

    Coordinates = intersection

    Data_1_Distance = 0

    Data_2_Distance = 0

    current_loc_1 = [0,0]

    current_loc_2 = [0,0]

    for i in Data_1:
        Direction = i[0]
        Length = int(i[1:])

        a = (Between_points(Direction,Length,current_loc_1, Coordinates))

        if (a[0]):
            Data_1_Distance += a[1]
            break

        else:
            b = Calculate_Next_Node(Direction, Length, current_loc_1,{})
            current_loc_1 = b[0]
            Data_2_Distance += Length

    for i in Data_2:
        Direction = i[0]
        Length = int(i[1:])

        a = (Between_points(Direction,Length,current_loc_2, Coordinates))

        if (a[0]):
            Data_2_Distance += a[1]
            break

        else:
            b = Calculate_Next_Node(Direction, Length, current_loc_2,{})
            current_loc_2 = b[0]
            Data_2_Distance += Length

    return Data_2_Distance + Data_1_Distance



def Part_2_Go(Data_1,Data_2,Dict1,Dict2):

    Intersections = Intersecting_Distances(Dict1,Dict2)

    Distances = []

    for i in Intersections:
        distance = Calculate_Distance(Data_1, Data_2,i)
        Distances.append(distance)

    #print(Distances)
    return min(Distances)







if __name__ == '__main__':



    Visited_1 = {}

    Visited_2 = {}

    f = open("input.txt", "r")
    Original_Data = []
    for line in f.readlines():
        Original_Data.append([x for x in line.split(",")])
    
    Central_Port = [0,0]

    #Original_Data = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],['U62','R66','U55','R34','D71','R55','D58','R83']]

    #Original_Data = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]

    First_Data = Original_Data[0][:]

    Second_Data = Original_Data[1][:]

    First = Part_1_Go(Central_Port, First_Data, Visited_1)

    Second = Part_1_Go(Central_Port, Second_Data, Visited_2)

    ans = Min_Distance(First,Second)

    
    print("First question, answer: {}".format(ans))

    ans = Part_2_Go(First_Data,Second_Data,First,Second)

    print("Second question, answer: {}".format(ans))



