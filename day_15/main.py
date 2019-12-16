#!/usr/bin/env python3

import random

import queue

class Graph():

    def __init__(self):
        self.vertices = {}
        self.tested_direction = {}
        self.not_explored = set()
        self.input = 0
        self.current_vertice = [0,0]
        self.Goal = None
        self.output = None
        self.previous_vertice = None
        self.prev_pos = None
        self.Add_If_Not_Visited()
    
    def Move(self):
        self.previous_vertice = self.current_vertice
        self.prev_pos = self.curr_pos
        if self.input == 1:
            self.current_vertice = self.current_vertice[0],self.current_vertice[1] + 1
        elif self.input == 2:
            self.current_vertice = self.current_vertice[0],self.current_vertice[1] - 1
        elif self.input == 3:
            self.current_vertice = self.current_vertice[0] - 1,self.current_vertice[1]
        elif self.input == 4:
            self.current_vertice = self.current_vertice[0] + 1,self.current_vertice[1]

    def Add_If_Not_Visited(self):
        self.curr_pos = '{},{}'.format(self.current_vertice[0],self.current_vertice[1])
        if self.curr_pos not in self.vertices.keys():
            self.vertices[self.curr_pos] = set()
            self.tested_direction[self.curr_pos] = set()
            self.not_explored.add(self.curr_pos)
    
    def Check_If_Fully_Visited(self):
        Length = len(self.tested_direction[self.curr_pos])

        if Length == 4 and self.curr_pos in self.not_explored:
            self.not_explored.remove(self.curr_pos)
    
    def Set_Goal(self):
        self.Goal = self.curr_pos
    
    def Completed(self):
        if len(self.not_explored) == 0:
            return True
        return False
    
    def Add_Vertice(self):
        self.vertices[self.curr_pos].add(self.prev_pos)
        self.vertices[self.prev_pos].add(self.curr_pos)

    def Add_Node(self):
        self.tested_direction[self.curr_pos].add(self.input)
        if self.output == 1:
            self.Move()
            self.Add_If_Not_Visited()
            self.Add_Vertice()
        elif self.output == 2:
            self.Move()
            self.Add_If_Not_Visited()
            self.Set_Goal()
            self.Add_Vertice()
        self.Check_If_Fully_Visited()
    
    def Set_Output(self, output):
        self.output = output

    def Set_Input(self):
        self.input = random.randint(1,4)
        if self.curr_pos in self.not_explored:
            while self.input in self.tested_direction[self.curr_pos]:
                self.input = random.randint(1,4)
        return self.input
    
    def Get_Goal(self):
        return self.Goal
    
    def Get_Vertices(self):
        return self.vertices


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
                Input = Node.Set_Input()
                Intcode, Indexes_Outside_Scope = Insert_At_Correct_Index(Intcode, Indexes_Outside_Scope, Input, Noun_Index, Noun_Mode, Base)

            elif OP_Code == 4:
                value = Get_Parameter_Value(Intcode, Indexes_Outside_Scope, Noun_Index, Noun_Mode, Base)
                Node.Set_Output(value)
                if Node.Completed():
                    return Node
                Node.Add_Node()

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

def Find_Closest_Paths(graph, start_pos):

    q = queue.Queue()
    current_dist = 0
    current_size = 0
    visited = set()
    distances = dict()
    q.put(start_pos)
    visited.add(start_pos)
    distances[current_dist] = set()
    distances[current_dist].add(start_pos)
    current_size = 1


    
    while not q.empty():
        if current_size == 0:
            current_dist += 1
            current_size = q.qsize()
            distances[current_dist] = set()
        
        current_node = q.get()
        current_size -= 1

        for vertice in graph[current_node]:
            if vertice not in visited:
                visited.add(vertice)
                distances[current_dist].add(vertice)
                q.put(vertice)
    
    return distances

        






def Program(Code):
    # Part 1
    Node = Graph()
    Node = Intcode_Program(Code,Node)

    Goal = Node.Get_Goal()

    Distances = Find_Closest_Paths(Node.Get_Vertices(), '0,0')

    for k,v in Distances.items():
        if Goal in v:
            dist = k
    
    print("Answer, Part 1: {}".format(dist))

    # Part 2

    Distances_2 = Find_Closest_Paths(Node.Get_Vertices(), Goal)

    time = max(Distances_2.keys())

    print("Answer, Part 2: {}".format(time))



if __name__ == '__main__':
    f = open("data.txt", "r")
    Data = [int(x) for x in f.read().split(",")]

    Program(Data.copy())