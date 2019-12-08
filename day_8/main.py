#!/usr/bin/env python3

def Split_To_Layers(Data, width, height):
    step = width*height
    return [Data[index:index+step] for index in range(0,len(Data),step)]

def Least_Zeroes(Layers):
    Layer = 0
    number = float('inf')
    for layer in Layers:
        if layer.count('0') < number:
            number = layer.count('0')
            Layer = layer
    return Layer

def Program(Data, width, height):
    Layers = Split_To_Layers(Data,width,height)
    Fewest_Zero_Layer = Least_Zeroes(Layers)
    ans = Fewest_Zero_Layer.count('1')*Fewest_Zero_Layer.count('2')
    print("Answer, Part 1: {}".format(ans))

    image = ['2']*width*height
    Length = range(len(image))
    for layer in Layers:
        for index in Length:
            if image[index] == '2':
                if layer[index] == '0':
                    image[index] = ' '
                elif layer[index] == '1':
                    image[index] = '█'
    image = "".join(image)
    print("Answer, Part 2:")
    for i in range(height):
        print("{}".format(image[i*width:(i+1)*width]))

if __name__ == '__main__':
    f = open("data.txt", "r")
    In_Data = f.read()
    Program(In_Data, 25, 6)