import argparse
import itertools
import random
import math

coordinates = {'A': [50,50], 'B': [50,50], 'C': [50,50], 'D': [50,50], 'E': [50,50]}
focal_points = ['A', 'B', 'C', 'D', 'E']
# focal_points = ['A']
angle_of_incidence = ['90', '60', '30']
directions = ['0', '15', '30', '45', '60', '75', '90', '105', '120', '135', '150', '165', '180', '195', '210', '225', '240', '255', '270', '285', '300', '315', '330', '345']
# directions = ['0', '45', '90', '135', '180', '225', '270']

perm = []
gcode = []

def randomize(user_index, angle):
    global perm
    if angle=='90':
        S = [focal_points, [angle], ['0']]
        perm = list(itertools.product(*S))
        perm.extend(perm)
    elif angle=='60' or angle=='30':
        S = [focal_points, [angle], directions]
        perm = list(itertools.product(*S))
    else:
        print("wrong angle")
    random.seed(user_index + int(angle))
    random.shuffle(perm)
    print("list all permutations: \n", perm)

def generate_gcode(angle):
    global gcode
    for p in perm:
        # coor = get_coor(p[0], angle, p[2])
        coor = coordinates[p[0]]
        gcode.append(f"G1 X{coor[0]} Y{coor[1]} Z15 F5000.0 ;\n")
        gcode.append(f"@pause {p} ;\n")

# def get_coor(prev_focal, angle, dir):
#     # 30 degree
#     if angle==angle_of_incidence[1]:
#         x = coordinates[prev_focal][0]-offset(dir)[0]
#         y = coordinates[prev_focal][1]-offset(dir)[1]
        
#         # Clamp x/y coordinates within 0-100
#         x = max(0, min(x, 100))
#         y = max(0, min(y, 100))

#         coor = [x, y]
#     # 60 & 90 degree
#     else:
#         coor = coordinates[prev_focal]
#     return coor

# def offset(angle):
#     angle = int(angle)
#     x_off = 2 * math.sin((math.radians(angle)))
#     y_off = 2 * math.cos((math.radians(angle)))
#     offset = round(x_off, 1), round(y_off, 1)
#     return offset

def write_order(filename):
    with open(filename, 'w', encoding = "utf-8") as f:
        f.write('focal_points, angle_of_incidence, directions\n')
        for p in perm:
            f.write(','.join(p))
            f.write('\n')

def write_gcode(filename):
    with open(filename, 'w', encoding = "utf-8") as f:
        f.write("G90 ;\n")
        f.write("M85 S0 ;\n")
        f.write("G1 X50 Y100 Z15 F5000.0 ;\n")
        f.write("@pause Start ;\n")
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
    parser.add_argument('-angle', '--angle', type=str, default='60')
    parser.add_argument('-gcode_out', '--gcode_filename', type=str, default='gcode.txt')
    parser.add_argument('-order_out', '--order_filename', type=str, default='order.txt')
    args = parser.parse_args()
    user_index = args.user_index
    angle = args.angle
    coordinates['A'] = args.A
    coordinates['B'] = args.B
    coordinates['C'] = args.C
    coordinates['D'] = args.D
    coordinates['E'] = args.E
    randomize(user_index, angle)
    generate_gcode(angle)
    write_order('./orders/' + str(user_index) + '_' + angle + 'deg' + '_' + args.order_filename)
    write_gcode('./gcodes/' + str(user_index) + '_' + angle + 'deg' + '_' + args.gcode_filename)
    
