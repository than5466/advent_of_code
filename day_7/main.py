#!/usr/bin/env python3

def Quotient(number, divisor):
    return number // divisor

def Remainder(number, divisor):
    return number % divisor

def Op_Code_1(noun,verb):
    return noun+verb


def Op_Code_2(noun, verb):
    return noun*verb


def Amplifier(Intcode, phase_setting, amplified_signal, pointer=0):

    Length = len(Intcode)
    Counter = pointer

    if phase_setting >= 0:
        inputs = [phase_setting,amplified_signal]
    else:
        inputs = [amplified_signal]
    input_index = 0

    while Counter < Length:

        First_Instruction = Intcode[Counter]
        OP_Code = Remainder(First_Instruction,100) # OP-koden är sista två
        Noun_Mode = Remainder(Quotient(First_Instruction,100),10)
        Verb_Mode = Remainder(Quotient(First_Instruction,1000),10)
        Insert_Mode = Remainder(Quotient(First_Instruction,10000),10)
        Noun_Index = Counter + 1
        Verb_Index = Counter + 2
        Insert = Counter + 3

        if OP_Code == 99:
            return False, Counter, Intcode

        elif OP_Code in [1,2]:
            Counter += 4

            Noun = Intcode[Noun_Index]
            Verb = Intcode[Verb_Index]
            
            if Noun_Mode == 0:
                Noun = Intcode[Noun]
            if Verb_Mode == 0:
                Verb = Intcode[Verb]
            if Insert_Mode == 0:
                Insert = Intcode[Insert]
            
            if OP_Code == 1:
                Intcode[Insert] = Op_Code_1(Verb,Noun)
            else:
                Intcode[Insert] = Op_Code_2(Verb,Noun)

        elif OP_Code in [3,4]:
            Counter += 2
            Insert = Intcode[Noun_Index]
            if OP_Code == 3:
                Input_Variable = inputs[input_index]
                input_index += 1
                Intcode[Insert] = Input_Variable
            else:
                if input_index == len(inputs):
                    return Intcode[Insert], Counter, Intcode
                else: 
                    return False, Counter, Intcode
        
        elif OP_Code in [5,6]:
            First_Parameter = Intcode[Noun_Index]
            Second_Parameter = Intcode[Verb_Index]
            if Noun_Mode == 0:
                First_Parameter = Intcode[First_Parameter]

            if Verb_Mode == 0:
                Second_Parameter = Intcode[Second_Parameter]

            if OP_Code == 5:
                if First_Parameter != 0:
                    Counter = Second_Parameter
                else:
                    Counter += 3
            
            if OP_Code == 6:
                if First_Parameter != 0:
                    Counter += 3
                else:
                    Counter = Second_Parameter
        
        elif OP_Code in [7,8]:
            First_Parameter = Intcode[Noun_Index]
            Second_Parameter = Intcode[Verb_Index]


            if Noun_Mode == 0:
                First_Parameter = Intcode[First_Parameter]
            if Verb_Mode == 0:
                Second_Parameter = Intcode[Second_Parameter]
            if Insert_Mode == 0:
                Insert = Intcode[Insert]

            if OP_Code == 7:
                if First_Parameter < Second_Parameter:
                    Var = 1
                else:
                    Var = 0
                Intcode[Insert] = Var

            if OP_Code == 8:
                if First_Parameter == Second_Parameter:
                    Var = 1
                else:
                    Var = 0
                Intcode[Insert] = Var
            
            Counter += 4


        else:
            print("Nu blev det tamejfan fel")
            break

def Calculate_Signal(Code, A, B, C, D, E, signal=0):
    First_amp = Amplifier(Code,A,signal)[0]
    Second_amp = Amplifier(Code,B,First_amp)[0]
    Third_amp = Amplifier(Code,C,Second_amp)[0]
    Forth_amp = Amplifier(Code,D,Third_amp)[0]
    Fifth_amp = Amplifier(Code,E,Forth_amp)[0]

    return Fifth_amp


def Calculate_Signal_2(A, B, C, D, E, Codes, signal=0, pointer=[0,0,0,0,0]):
    First_amp, first_pointer, IntCode_A = Amplifier(Codes[0],A,signal,pointer[0])
    Second_amp, second_pointer, IntCode_B = Amplifier(Codes[1],B,First_amp,pointer[1])
    Third_amp, third_pointer, IntCode_C = Amplifier(Codes[2],C,Second_amp,pointer[2])
    Forth_amp, forth_pointer, IntCode_D = Amplifier(Codes[3],D,Third_amp,pointer[3])
    Fifth_amp, fifth_pointer, IntCode_E = Amplifier(Codes[4],E,Forth_amp,pointer[4])

    pointers = [first_pointer, second_pointer, third_pointer, forth_pointer, fifth_pointer]
    IntCodes = [IntCode_A, IntCode_B, IntCode_C, IntCode_D, IntCode_E]
    return Fifth_amp, pointers, IntCodes
    
def Program_1(IntCode):

    All_outputs = []


    for A in range(5):
        for B in range(5):
            for C in range(5):
                for D in range(5):
                    for E in range(5):
                        Check_List = list(dict.fromkeys([A,B,C,D,E]))
                        if len(Check_List) == 5:
                            signal = Calculate_Signal(IntCode,A,B,C,D,E)
                            All_outputs.append(signal)

    max_output = max(All_outputs)
    return max_output                          

def Program_2(IntCode):

    All_outputs = []

    for A in range(5,10):
        for B in range(5,10):
            for C in range(5,10):
                for D in range(5,10):
                    for E in range(5,10):
                        Check_List = list(dict.fromkeys([A,B,C,D,E]))
                        if len(Check_List) == 5:
                            past_signal = 0
                            IntCodes = [IntCode.copy(), IntCode.copy(), IntCode.copy(), IntCode.copy(), IntCode.copy()]
                            signal, pointers, IntCodes = Calculate_Signal_2(A,B,C,D,E,IntCodes)
                            while signal:
                                past_signal = signal
                                signal, pointers, IntCodes = Calculate_Signal_2(-1,-1,-1,-1,-1,IntCodes, signal, pointers)
                            All_outputs.append(past_signal)

    
    max_output = max(All_outputs)

    return max_output            

if __name__ == '__main__':
    f = open("data.txt", "r")
    Original_Data = [int(x) for x in f.read().split(",")]

    Data = Original_Data[:]

    #Data = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

    #Data = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]

    #Data = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

    part_1 = Program_1(Data)

    print("Answer, Part 1: {}".format(part_1))

    #Data = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

    #Data = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    part_2 = Program_2(Data)

    print("Answer, Part 2: {}".format(part_2))

