from asyncore import write
import os
import sys

def writeFile(focal, data):
    output = open(focal + "_data.txt", "a")

    output.write('PERCEIVED SOURCE DIRECTIONS' + '\n')
    for sample in data:
        output.write(str(sample[0]) + '\n')

    output.write('CONFIDENCE SCORES' + '\n')
    for sample in data:
        output.write(str(sample[1]) + '\n')

    output.close()

def mergeFiles(order, data):
    f1 = open(os.path.join(sys.path[0], order), encoding = "utf8")
    f2 = open(os.path.join(sys.path[0], data), encoding = "utf8")
    next(f1)
    
    samples_sorted = []
    for line in f1:
        sample = line.strip().split(',')
        del sample[1]
        sample[1] = int(sample[1])

        value = next(f2).strip().split(',')
        value = [int(e) for e in value]

        samples_sorted.append(sample + value)

    samples_sorted = sorted(samples_sorted)

    f1.close()
    f2.close()
    
    output = open("complete_data.txt", "a")
    for sample in samples_sorted:
        output.write(str(sample) + '\n')
    output.close()

    A, B, C, D, E = [], [], [], [], []
    for sample in samples_sorted:
        if sample[0] == 'A':
            A.append(sample[2:])
        if sample[0] == 'B':
            B.append(sample[2:])
        if sample[0] == 'C':
            C.append(sample[2:])
        if sample[0] == 'D':
            D.append(sample[2:])
        if sample[0] == 'E':
            E.append(sample[2:])
    
    writeFile('A', A)
    writeFile('B', B)
    writeFile('C', C)
    writeFile('D', D)
    writeFile('E', E)

if __name__=='__main__':
    mergeFiles("order.txt", "data.txt")