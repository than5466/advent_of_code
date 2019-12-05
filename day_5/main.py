#!/usr/bin/env python3

def Quotient(number, divisor):
    return number // divisor

def Remainder(number, divisor):
    return number % divisor

def Op_Code_1(noun,verb):
    return noun+verb


def Op_Code_2(noun, verb):
    return noun*verb

def Program(Input):

    Length = len(Input)
    Counter = 0

    while Counter < Length:

        First_Instruction = Input[Counter]
        OP_Code = Remainder(First_Instruction,100) # OP-koden är sista två
        Noun_Mode = Remainder(Quotient(First_Instruction,100),10)
        Verb_Mode = Remainder(Quotient(First_Instruction,1000),10)
        Insert_Mode = Remainder(Quotient(First_Instruction,10000),10)
        Noun_Index = Counter + 1
        Verb_Index = Counter + 2
        Insert = Counter + 3

        if OP_Code == 99:
            break

        elif OP_Code in [1,2]:
            Counter += 4

            Noun = Input[Noun_Index]
            Verb = Input[Verb_Index]
            
            if Noun_Mode == 0:
                Noun = Input[Noun]
            if Verb_Mode == 0:
                Verb = Input[Verb]
            if Insert_Mode == 0:
                Insert = Input[Insert]
            
            if OP_Code == 1:
                Input[Insert] = Op_Code_1(Verb,Noun)
            else:
                Input[Insert] = Op_Code_2(Verb,Noun)

        elif OP_Code in [3,4]:
            Counter += 2
            Insert = Input[Noun_Index]
            if OP_Code == 3:
                Input_Variable = int(input("Make an input: "))
                Input[Insert] = Input_Variable
            else:
                print(Input[Insert])
        
        elif OP_Code in [5,6]:
            First_Parameter = Input[Noun_Index]
            Second_Parameter = Input[Verb_Index]
            if Noun_Mode == 0:
                First_Parameter = Input[First_Parameter]

            if Verb_Mode == 0:
                Second_Parameter = Input[Second_Parameter]

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
            First_Parameter = Input[Noun_Index]
            Second_Parameter = Input[Verb_Index]


            if Noun_Mode == 0:
                First_Parameter = Input[First_Parameter]
            if Verb_Mode == 0:
                Second_Parameter = Input[Second_Parameter]
            if Insert_Mode == 0:
                Insert = Input[Insert]

            if OP_Code == 7:
                if First_Parameter < Second_Parameter:
                    Var = 1
                else:
                    Var = 0
                Input[Insert] = Var

            if OP_Code == 8:
                if First_Parameter == Second_Parameter:
                    Var = 1
                else:
                    Var = 0
                Input[Insert] = Var
            
            Counter += 4


        else:
            print("Nu blev det tamejfan fel")
            break

    



if __name__ == '__main__':
    f = open("data.txt", "r")
    Original_Data = [int(x) for x in f.read().split(",")]

    Data = Original_Data[:]

    #Data = [3,3,1108,-1,8,3,4,3,99]

    Program(Data)


