#!/usr/bin/env python3



class Board():

    def __init__(self):
        self.board = [[]]
        self.pointer = 0
        self.last_output = None
    
    def Update_Output(self, value):
        self.last_output = value
    
    def Update_Board(self):
        if self.last_output == 10:
            self.pointer += 1
            self.board.append([])
        elif self.last_output == 35:
            self.board[self.pointer].append('#')
        elif self.last_output == 46:
            self.board[self.pointer].append('.')
        else: 
            self.board[self.pointer].append('>')
    
    def Update(self,value):
        self.Update_Output(value)
        self.Update_Board()
    
    def Show_Board(self):
        for row in self.board:
            print("".join(row))
    
    def Get_Board(self):
        return self.board


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
    

def Intcode_Program(Intcode, Node):
    Pointer = 0
    Base = 0
    Indexes_Outside_Scope = {}

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
            return Node

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
                #Intcode, Indexes_Outside_Scope = Insert_At_Correct_Index(Intcode, Indexes_Outside_Scope, Input, Noun_Index, Noun_Mode, Base)
                return

            elif OP_Code == 4:
                value = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
                Node.Update(value)
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


def Sum_Of_Alignments(board):
    cumulative_sum = 0

    height = len(board)

    for row in range(1,height-1):
        width = len(board[row])
        for col in range(1,width-1):
            if Scaffold(board,col,row):
                if Intersection(board,col,row):
                    cumulative_sum += col*row
    
    return cumulative_sum


def Intersection(board,x_coord,y_coord):
    if Scaffold(board,x_coord-1,y_coord) and Scaffold(board,x_coord+1,y_coord) and Scaffold(board,x_coord,y_coord-1) and Scaffold(board,x_coord,y_coord+1):
        return True
    return False

def Scaffold(board,x_coord,y_coord):
    return board[y_coord][x_coord] == '#'
    

def Part_1(Code):
    #Part 1

    Node = Board()
    Node = Intcode_Program(Code,Node)

    Node.Show_Board()

    Alignment_Sum = Sum_Of_Alignments(Node.Get_Board())

    print("Answer, Part 1: {}".format(Alignment_Sum))



if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [int(x) for x in f.read().split(",")]

    Part_1(Data.copy())