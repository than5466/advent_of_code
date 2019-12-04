#!/usr/bin/env python3

def Stringify(Number):
    
    return str(Number)



def Strictly_Increasing(Number):

    Number_of_Checks = len(Number)-1
    for index in range(Number_of_Checks):
        if Number[index] > Number[index+1]:
            return False

    return True


def Reoccuring_Digits(Number):
    
    i = Number[0]
    count = 1
    while count < len(Number):
        if Number[count] == i:
            count += 1
        
        else:
            break
    
    return count


def Contains_Duplicate(Number):

    End = len(Number) - 1
    Current = 0

    while Current < End:
        repeated = Reoccuring_Digits(Number[Current:])
        if repeated >= 2:
            return True

        Current += repeated

    return False


def Contains_Exact_Duplicate(Number):

    End = len(Number) - 1
    Current = 0

    while Current < End:
        repeated = Reoccuring_Digits(Number[Current:])
        if repeated == 2:
            return True

        Current += repeated

    return False


def Program():


    Start = 172851
    End = 675869 + 1
    Candidates_Part_1 = []
    Candidates_Part_2 = []

    for num in range(Start, End):
        num_string = Stringify(num)

        if Strictly_Increasing(num_string):
            if Contains_Duplicate(num_string):
                Candidates_Part_1.append(num_string)

            if Contains_Exact_Duplicate(num_string):
                Candidates_Part_2.append(num_string)

    ans_part_1 = len(Candidates_Part_1)
    print("First question, answer: {}".format(ans_part_1))

    ans_part_2 = len(Candidates_Part_2)
    print("Second question, answer: {}".format(ans_part_2))


if __name__ == '__main__':

    Program()



