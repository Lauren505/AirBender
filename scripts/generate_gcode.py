import argparse
import itertools
import random

user_index = 0
coordinates = {'A': [50,50], 'B': [50,50], 'C': [50,50], 'D': [50,50], 'E': [50,50]}
focal_points = ['A', 'B', 'C', 'D', 'E']
angle_of_incidence = ['0', '30', '60']
directions = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
S = [focal_points, angle_of_incidence[1:], directions]
perm = list(itertools.product(*S))
perm.extend(list(itertools.product(focal_points, [angle_of_incidence[0]])))
gcode = []
random.seed(user_index) # user index

def randomize():
    random.shuffle(perm)
    print("list all permutations: \n", perm)

def generate_gcode():
    last = perm[0][0]
    coor = coordinates[last]
    gcode.append(f"G0 X{coor[0]} Y{coor[1]} ;\n")
    gcode.append(f"@pause {perm[0]} ")
    for p in perm[1:]:
        if (p[0]==last):
            gcode.append(f"{p} ")
        else:
            last = p[0]
            coor = coordinates[last]
            gcode.append(f";\nG0 X{coor[0]} Y{coor[1]} ;\n")
            gcode.append(f"@pause {p} ")

def write_order(filename):
    with open(filename, 'w', encoding = "utf-8") as f:
        for p in perm:
            f.write(','.join(p))
            f.write('\n')

def write_gcode(filename):
    with open(filename, 'w', encoding = "utf-8") as f:
        f.write("G28 ;\n")
        f.write("G90 ;\n")
        for line in gcode:
            f.write(line)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-idx', '--user_index', type=int, default=0)
    parser.add_argument('-a', '--A', type=int, nargs=2, default=[50,50])
    parser.add_argument('-b', '--B', type=int, nargs=2, default=[50,50])
    parser.add_argument('-c', '--C', type=int, nargs=2, default=[50,50])
    parser.add_argument('-d', '--D', type=int, nargs=2, default=[50,50])
    parser.add_argument('-e', '--E', type=int, nargs=2, default=[50,50])
    parser.add_argument('-gcode_out', '--gcode_filename', type=str, default='gcode.txt')
    parser.add_argument('-order_out', '--order_filename', type=str, default='order.txt')
    args = parser.parse_args()
    user_index = args.user_index
    coordinates['A'] = args.A
    coordinates['B'] = args.B
    coordinates['C'] = args.C
    coordinates['D'] = args.D
    coordinates['E'] = args.E
    randomize()
    generate_gcode()
    write_order('./orders/' + str(user_index) + '_' + args.order_filename)
    write_gcode('./gcodes/' + str(user_index) + '_' + args.gcode_filename)
    
