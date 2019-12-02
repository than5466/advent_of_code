#!/usr/bin/env python3

import math

def Current_Indexes(lst, int):
    return lst[int:int+4]


def Op_Code_1(lst, index_1, index_2):
    return lst[index_1]+lst[index_2]


def Op_Code_2(lst, index_1,index_2):
    return lst[index_1]*lst[index_2]


def Update_Data(lst, noun, verb):
    lst[1] = noun
    lst[2] = verb
    return lst

def Solution(lst, noun, verb):

    lst = Update_Data(lst, noun, verb)

    Counter = 0

    while Counter < len(lst):

        Index_0 = lst[Counter]

        if Index_0 == 99:
            break

        Index_1, Index_2, Index_3 = lst[Counter+1], lst[Counter+2], lst[Counter+3]

        if Index_0 == 1:
            value = Op_Code_1(lst,Index_1,Index_2)
            lst[Index_3] = value

        elif Index_0 == 2:
            value = Op_Code_2(lst,Index_1,Index_2)
            lst[Index_3] = value
        
        Counter += 4
    
    return lst

def Part_2(lst, ans, max):
    for i in range(max):
        for j in range(max):
            data = lst[:]
            var = Solution(data,i,j)

            if var[0] == ans:
                return i, j


if __name__ == '__main__':
    f = open("data.txt", "r")
    Original_Data = [int(x) for x in f.read().split(",")]

    Data_1 = Original_Data[:]

    Part_1_Data = Solution(Data_1, 12, 2)

    print(Part_1_Data[0])

    Data_2 = Original_Data[:]

    Part_2_Data = Part_2(Data_2,19690720,100)

    print ("The answer is " + str(100*Part_2_Data[0]+Part_2_Data[1]))


