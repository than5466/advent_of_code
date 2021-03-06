#!/usr/bin/env python3


def Quotient(number, divisor):
    return number // divisor


def Remainder(number, divisor):
    return number % divisor


def Get_Value(Code, Dict, Index):
    if Index < len(Code):
        return Code[Index]
    elif Index in Dict.keys():
        return Dict[Index]
    return 0


def Get_Parameter_Value(Code, Dict, Index, Mode, Base):
    if Mode == 0:
        Index = Get_Value(Code, Dict, Index)
    elif Mode == 2:
        Index = Get_Value(Code, Dict, Index) + Base
    elif Mode != 1:
        raise RuntimeError("Parameter mode {} is not supported".format(Mode))
    return Get_Value(Code, Dict, Index)


def Insert(Code,Dict,Value,Index):
    if Index < len(Code):
        Code[Index] = Value
    else:
        Dict[Index] = Value
    return Code, Dict


def Insert_At_Correct_Index(Code, Dict, Value, Index, Mode, Base):
    if Mode == 0:
        Index = Get_Value(Code, Dict, Index)
    elif Mode == 2:
        Index = Get_Value(Code, Dict, Index) + Base
    return Insert(Code,Dict,Value,Index)


def Intcode_Program(Intcode, Input):
    Pointer = 0
    Base = 0
    Indexes_Outside_Scope = {}
    value = 0
    Input_Count = 0
    Max_Inputs = 1
    Update_Count = 0
    Max_Value_Updates = 1

    while True:
        First_Instruction = Get_Value(Intcode, Indexes_Outside_Scope, Pointer)
        OP_Code = Remainder(First_Instruction,100) 
        Noun_Mode = Remainder(Quotient(First_Instruction,100),10)
        Verb_Mode = Remainder(Quotient(First_Instruction,1000),10)
        Insert_Mode = Remainder(Quotient(First_Instruction,10000),10)
        Noun_Index = Pointer + 1
        Verb_Index = Pointer + 2
        Insert_Index = Pointer + 3
        
        if OP_Code == 99:
            return value

        elif OP_Code in [1,2,7,8]:
            Noun = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
            Verb = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Verb_Index, Verb_Mode, Base)    
            if OP_Code == 1:
                Var = Noun+Verb
            elif OP_Code == 2:
                Var = Noun*Verb
            elif OP_Code == 7:
                Var = int(Noun < Verb)
            elif OP_Code == 8:
                Var = int(Noun == Verb)
            Intcode, Indexes_Outside_Scope = Insert_At_Correct_Index(Intcode, Indexes_Outside_Scope, Var, Insert_Index, Insert_Mode, Base)
            Pointer += 4

        elif OP_Code in [3,4]:
            if OP_Code == 3:
                Input_Count += 1
                if Input_Count > Max_Inputs :
                    raise RuntimeError("Only a maximum of {} inputs allowed, this was the {} input".format(Max_Inputs, Input_Count))
                Intcode, Indexes_Outside_Scope = Insert_At_Correct_Index(Intcode, Indexes_Outside_Scope, Input, Noun_Index, Noun_Mode, Base)
            elif OP_Code == 4:
                Update_Count += 1
                if Update_Count > Max_Value_Updates:
                    raise RuntimeError("Only a maximum of {} outputs allowed, this was the {} output".format(Max_Value_Updates, Update_Count))
                value = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
            Pointer += 2
        
        elif OP_Code in [5,6]:
            First_Parameter = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
            Second_Parameter = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Verb_Index, Verb_Mode, Base)
            if OP_Code == 5:
                if First_Parameter > 0:
                    Pointer = Second_Parameter
                else:
                    Pointer += 3
            elif OP_Code == 6:
                if First_Parameter != 0:
                    Pointer += 3
                else:
                    Pointer = Second_Parameter
        
        elif OP_Code == 9:
            Parameter = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
            Base += Parameter
            Pointer += 2

        else:
            raise RuntimeError("OP_Code {} not allowed".format(OP_Code))

def Program(Code):
    #Part 1
    a = Intcode_Program(Code.copy(),1)
    print("Answer, Part 1: {}".format(a))

    #Part 2
    b = Intcode_Program(Code.copy(),2)
    print("Answer, Part 2: {}".format(b))

if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [int(x) for x in f.read().split(",")]

    Program(Data)

