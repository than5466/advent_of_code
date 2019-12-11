#!/usr/bin/env python3

class Paint_Node():

    def __init__(self):
        self.current_pos = [0,0]
        self.painted_positions = {}
        self.direction = 'Up'
        self.possible_directions = ['Up','Right','Down', 'Left', 'Up']
        self.mode = 'color'
        self.input_value = 0
        self.number_painted = 0
    
    def turn_left(self):
        for i in range(1,len(self.possible_directions)):
            if self.possible_directions[i] == self.direction:
                self.direction = self.possible_directions[i-1]
                break
    
    def turn_right(self):
        for i in range(len(self.possible_directions)-1):
            if self.possible_directions[i] == self.direction:
                self.direction = self.possible_directions[i+1]
                break

    def turn(self,value):
        if value == 0:
            self.turn_left()
        elif value == 1:
            self.turn_right()
    
    def Move(self):
        if self.direction == 'Right':
            self.current_pos[0] += 1
        elif self.direction == 'Left':
            self.current_pos[0] -= 1
        elif self.direction == 'Up':
            self.current_pos[1] -= 1
        elif self.direction == 'Down':
            self.current_pos[1] += 1
        else: 
            print('vad nu')

    def Paint_Position(self, color_int):
        pos_as_string = "({},{})".format(self.current_pos[0],self.current_pos[1])
        if pos_as_string not in self.painted_positions:
            self.number_painted += 1
        if color_int == 0:
            self.painted_positions[pos_as_string] = 'black'
        elif color_int == 1:
            self.painted_positions[pos_as_string] = 'white'
        else:
            print('vafalls')

    def Change_Mode(self):
        if self.mode == 'color':
            self.mode = 'turn'
        elif self.mode == 'turn':
            self.mode = 'color'
    
    def Determine_Input(self):
        pos_as_string = "({},{})".format(self.current_pos[0],self.current_pos[1])
        if pos_as_string in self.painted_positions:
            if self.painted_positions[pos_as_string] == 'white':
                self.input_value = 1
            else:
                self.input_value = 0
        else:
            self.input_value = 0
    
    def Number_Painted(self):
        return self.number_painted
    
    def Get_Current_Position(self):
        return self.current_pos
    
    def Get_Current_Direction(self):
        return self.direction
    
    def Get_Mode(self):
        return self.mode
    
    def Get_Input(self):
        return self.input_value

    def Get_All_Painted_Positions(self):
        return self.painted_positions


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
                Node.Determine_Input()
                Input = Node.Get_Input()
                Intcode, Indexes_Outside_Scope = Insert_At_Correct_Index(Intcode, Indexes_Outside_Scope, Input, Noun_Index, Noun_Mode, Base)
            elif OP_Code == 4:
                value = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
                if Node.Get_Mode() == 'color':
                    Node.Paint_Position(value)
                elif Node.Get_Mode() == 'turn':
                    Node.turn(value)
                    Node.Move()
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

def Program(Code):
    #Part 1
    Node = Paint_Node()
    Node = Intcode_Program(Code,Node)
    ans = Node.Number_Painted()

    print("Answer, Part 1: {}".format(ans))


def Program_2(Code):
    #Part 2
    Node = Paint_Node()
    Node.Paint_Position(1)

    Node = Intcode_Program(Code,Node)
    board = Node.Get_All_Painted_Positions()

    indexes_of_white_panels = []


    for k,v in board.items():
        if v == 'white':
            index = k[1:-1].split(',')
            index[0],index[1] = int(index[0]),int(index[1])
            indexes_of_white_panels.append(index)

    sorted_by_x_coord, sorted_by_y_coord = indexes_of_white_panels.copy(), indexes_of_white_panels.copy()
    
    sorted_by_x_coord.sort(key = lambda x: x[0]), sorted_by_y_coord.sort(key = lambda y: y[1])
    min_x, max_x, min_y, max_y = sorted_by_x_coord[0][0], sorted_by_x_coord[-1][0], sorted_by_y_coord[0][1], sorted_by_y_coord[-1][1]

    x_relative, y_relative = - min_x, - min_y
    x_diff, y_diff = max_x - min_x + 1, max_y - min_y + 1
    Finished_Row = [' ']*x_diff
    Finished_Board = []

    for i in range(y_diff):
        Finished_Board.append(Finished_Row.copy())

    for Tuple in indexes_of_white_panels:
        x = Tuple[0] + x_relative
        y = Tuple[1] + y_relative
        Finished_Board[y][x] = '#'

    print("Answer, Part 2:")
    for row in Finished_Board:
        row = "".join(row)
        print(row)





if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [int(x) for x in f.read().split(",")]

    Program(Data.copy())

    Program_2(Data.copy())
    
