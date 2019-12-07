#!/usr/bin/env python3

class Amplifier_State():
    def __init__(self,setting, code):
        self.IntCode = code
        self.Pointer = 0
        self.Phase_Setting = setting
        self.Value = 0
        self.Phase_Status = True
    
    def setCode(self,code):
        self.IntCode = code

    def setValue(self,value):
        self.Value = value
    
    def setPointer(self,pointer):
        self.Pointer = pointer

    def setStatusFalse(self):
        self.Phase_Status = False

    def getCode(self):
        return self.IntCode

    def getValue(self):
        return self.Value

    def getPointer(self):
        return self.Pointer

    def getStatus(self):
        return self.Phase_Status

    def getPhaseSetting(self):
        return self.Phase_Setting


def Quotient(number, divisor):
    return number // divisor

def Remainder(number, divisor):
    return number % divisor

def Amplifier(Node):
    Length = len(Node.getCode())
    Counter = Node.getPointer()
    Status = Node.getStatus()
    phase_setting = Node.getPhaseSetting()
    amplified_signal = Node.getValue()
    Intcode = Node.getCode()

    if Status:
        inputs = [phase_setting,amplified_signal]
    else:
        inputs = [amplified_signal]
    input_index = 0

    while Counter < Length:

        First_Instruction = Intcode[Counter]
        OP_Code = Remainder(First_Instruction,100) 
        Noun_Mode = Remainder(Quotient(First_Instruction,100),10)
        Verb_Mode = Remainder(Quotient(First_Instruction,1000),10)
        Insert_Mode = Remainder(Quotient(First_Instruction,10000),10)
        Noun_Index = Counter + 1
        Verb_Index = Counter + 2
        Insert = Counter + 3

        if OP_Code == 99:
            Node.setValue(False)
            return Node

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
                Intcode[Insert] = Noun+Verb
            else:
                Intcode[Insert] = Noun*Verb

        elif OP_Code in [3,4]:
            Counter += 2
            Insert = Intcode[Noun_Index]
            if OP_Code == 3:
                Input_Variable = inputs[input_index]
                input_index += 1
                Intcode[Insert] = Input_Variable
            else:
                if  input_index == len(inputs):
                    Node.setValue(Intcode[Insert])
                    Node.setStatusFalse()
                    Node.setPointer(Counter)
                    Node.setCode(Intcode)
                    return Node
        
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

def Calculate_Signal(States):
    A,B,C,D,E = States
    A = Amplifier(A)
    B.setValue(A.getValue())
    B = Amplifier(B)
    C.setValue(B.getValue())
    C = Amplifier(C)
    D.setValue(C.getValue())
    D = Amplifier(D)
    E.setValue(D.getValue())
    E = Amplifier(E)
    A.setValue(E.getValue())
    return A,B,C,D,E

def Program_1(IntCode):

    All_outputs = []


    for A in range(5):
        for B in range(5):
            for C in range(5):
                for D in range(5):
                    for E in range(5):
                        Check_List = list(dict.fromkeys([A,B,C,D,E]))
                        if len(Check_List) == 5:
                            A_State, B_State = Amplifier_State(A,IntCode.copy()),Amplifier_State(B,IntCode.copy())
                            C_State, D_State, E_State = Amplifier_State(C,IntCode.copy()),Amplifier_State(D,IntCode.copy()),Amplifier_State(E,IntCode.copy())
                            States = [A_State,B_State,C_State,D_State,E_State]
                            States = Calculate_Signal(States)
                            Signal = States[4].getValue()
                            All_outputs.append(Signal)

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
                            A_State, B_State = Amplifier_State(A,IntCode.copy()),Amplifier_State(B,IntCode.copy())
                            C_State, D_State, E_State = Amplifier_State(C,IntCode.copy()),Amplifier_State(D,IntCode.copy()),Amplifier_State(E,IntCode.copy())
                            States = [A_State,B_State,C_State,D_State,E_State]
                            States = Calculate_Signal(States)
                            signal = States[4].getValue()
                            while True:
                                past_signal = signal
                                States = Calculate_Signal(States)
                                if States[0].getValue():
                                    signal = States[4].getValue()
                                else:
                                    break
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