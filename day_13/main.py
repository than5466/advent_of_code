#!/usr/bin/env python3



class Board():

    def __init__(self):
        self.board = [[' ' for i in range(46)] for j in range(26)]
        self.x = 0
        self.y = 0
        self.input_value = 0
        self.number_painted = 0
        self.mode = 'x_coord_out'
        self.score = 0

    def Set_Pos_x(self,x_coord):
        self.x = x_coord
    
    def Set_Pos_y(self,y_coord):
        self.y = y_coord

    def Paint_Position(self, int_id):
        if int_id == 0:
            self.board[self.y][self.x] = ' '
        elif int_id == 1:
            self.board[self.y][self.x] = '█'
        elif int_id == 2:
            self.board[self.y][self.x] = '#'
        elif int_id == 3:
            self.board[self.y][self.x] = '-'
        elif int_id == 4:
            self.board[self.y][self.x] = 'o'
        else:
            self.score = int_id

    def Change_Mode(self):
        if self.mode == 'x_coord_out':
            self.mode = 'y_coord_out'
        elif self.mode == 'y_coord_out':
            self.mode = 'tile_id'
        elif self.mode == 'tile_id':
            self.mode = 'x_coord_out'
    
    def Number_Painted(self):
        return self.number_painted
    
    def Get_Current_Position(self):
        return [self.x,self.y]
    
    def Get_Mode(self):
        return self.mode
    
    def Get_Input(self):
        return self.input_value

    def Print_Board(self):
        for row in self.board:
            print("".join(row))
        print(self.score)
    
    def Get_Board(self):
        board = ''
        for row in self.board:
            board += "".join(row) + "\n"
        return board

    def Get_Score(self):
        return self.score

    def Get_Block_Count(self):
        blockcount = 0

        for row in self.board:
            for position in row:
                if position == "#":
                    blockcount += 1
        return blockcount
    
    def Get_Paddle_X_Index(self):

        for row_num in range(len(self.board)):
            for index in range(len(self.board[row_num])):
                if self.board[row_num][index] == '-':
                    return index
    
    def Get_Ball_X_Index(self):

        for row_num in range(len(self.board)):
            for index in range(len(self.board[row_num])):
                if self.board[row_num][index] == 'o':
                    return index

    def Set_Input(self):

        ball_index = self.Get_Ball_X_Index()
        paddle_index = self.Get_Paddle_X_Index()

        if ball_index < paddle_index:
            self.input_value = -1
        
        elif ball_index == paddle_index:
            self.input_value = 0
        
        elif ball_index > paddle_index:
            self.input_value = 1

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
                Node.Set_Input()
                Input = Node.Get_Input()
                Intcode, Indexes_Outside_Scope = Insert_At_Correct_Index(Intcode, Indexes_Outside_Scope, Input, Noun_Index, Noun_Mode, Base)

            elif OP_Code == 4:
                value = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
                if Node.Get_Mode() == 'x_coord_out':
                    Node.Set_Pos_x(value)
                elif Node.Get_Mode() == 'y_coord_out':
                    Node.Set_Pos_y(value)
                elif Node.Get_Mode() == 'tile_id':
                    Node.Paint_Position(value)
                Node.Change_Mode()
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

def Part_1(Code):
    #Part 1
    Node = Board()
    Node = Intcode_Program(Code,Node)

    amount_of_blocks = Node.Get_Block_Count()

    print("Answer, Part 1: {}".format(amount_of_blocks))

def Part_2(Code):
    Code[0] = 2

    Node = Board()
    Node = Intcode_Program(Code,Node)

    score = Node.Get_Score()

    print("Answer, Part 2: {}".format(score))



if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [int(x) for x in f.read().split(",")]

    Part_1(Data.copy())
    Part_2(Data.copy())
