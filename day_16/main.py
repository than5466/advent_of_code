#!/usr/bin/env python3

def repetition(number_seq, step):

    current_pattern = 1
    new_number = 0

    for n in range(step -1, len(number_seq), 2*step):
        new_digit = sum(number_seq[n:n+step])
        new_number += current_pattern * new_digit
        current_pattern *= -1

    return abs(new_number) % 10


def FFT(number):
    next_phase_number = []

    for i in range(1,len(number)+1):
        next_phase_number.append(repetition(number,i))
    
    return next_phase_number

def FFT_Part_2(number_seq):
    next_phase_number = []
    cumulative = sum(number_seq)


    for n in number_seq:
        curr_pos = cumulative % 10
        next_phase_number.append(curr_pos)
        cumulative -= n
    return next_phase_number

def Program(number, phases):
    # Part 1

    count = phases

    Sequence_1 = number.copy()
    while count > 0:
        Sequence_1 = FFT(Sequence_1)
        count -= 1
    
    ans = "".join(map(str, Sequence_1[:8]))
    print('Answer, Part 1: {}'.format(ans))

    # Part 2
    # Inital offset is more than half. for an index position x,
    # where x is larger than half of than the length of the number,
    # we only need to sum up all the elements from index x.

    count = phases
    offset = 0

    for i in range(7):
        offset = offset*10 + number[i]
    Sequence_2 = (number*10000)[offset:]
    while count > 0:
        Sequence_2 = FFT_Part_2(Sequence_2)
        count -= 1
    
    ans = "".join(map(str, Sequence_2[:8]))

    print('Answer, Part 2: {}'.format(ans))
    

if __name__ == '__main__':
    f = open("data.txt", "r")
    Num_seq = [int(x) for x in f.read().rstrip()]

    Num_seq = Num_seq

    Program(Num_seq,100)