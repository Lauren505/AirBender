import argparse
import itertools
import random
import math

coordinates = {'A': [50,50], 'B': [50,50], 'C': [50,50], 'D': [50,50], 'E': [50,50]}
focal_points = ['A', 'B', 'C', 'D', 'E']
angle_of_incidence = ['90', '60', '30']
directions = ['0', '15', '30', '45', '60', '75', '90', '105', '120', '135', '150', '165', '180', '195', '210', '225', '240', '255', '270', '285', '300', '315', '330', '345']
perm = []
gcode = []

def randomize(user_index, angle):
    global perm
    if angle==angle_of_incidence[0]:
        S = [focal_points, [angle_of_incidence[0]], ['0']]
        perm = list(itertools.product(*S))
        perm.extend(perm)
    elif angle==angle_of_incidence[1]:
        S = [focal_points, [angle_of_incidence[1]], directions]
        perm = list(itertools.product(*S))
    elif angle==angle_of_incidence[2]:
        S = [focal_points, [angle_of_incidence[2]], directions]
        perm = list(itertools.product(*S))
    else:
        print("wrong angle")
    random.seed(user_index + int(angle)) # user index
    random.shuffle(perm)
    print("list all permutations: \n", perm)

def generate_gcode(angle):
    global gcode
    if angle==angle_of_incidence[2]:
        for p in perm:
            coor = get_coor(p[0], angle, p[2])
            gcode.append(f"G0 X{coor[0]} Y{coor[1]} ;\n")
            gcode.append(f"@pause {p} ;\n")
    else:
        prev_focal = perm[0][0]
        coor = get_coor(prev_focal, angle, perm[0][2])
        gcode.append(f"G0 X{coor[0]} Y{coor[1]} ;\n")
        gcode.append(f"@pause {perm[0]} ")
        for p in perm[1:]:
            if (p[0]==prev_focal):
                gcode.append(f"{p} ")
            else:
                prev_focal = p[0]
                coor = get_coor(prev_focal, angle, p[2])
                gcode.append(f";\nG0 X{coor[0]} Y{coor[1]} ;\n")
                gcode.append(f"@pause {p} ")

def get_coor(prev_focal, angle, dir):
    # 30 degree
    if angle==angle_of_incidence[2]:
        x = coordinates[prev_focal][0]+offset(dir)[0]
        y = coordinates[prev_focal][1]+offset(dir)[1]
        if x>100: x=100
        elif x<0: x=0
        if y>100: y=100
        elif y<0: y=0
        coor = [x, y]
    # 60 & 90 degree
    else:
        coor = coordinates[prev_focal]
    return coor

def offset(angle):
    angle = int(angle)
    x_off = 25 * math.sin((math.radians(angle)))
    y_off = 25 * math.cos((math.radians(angle)))
    offset = round(x_off, 1), round(y_off, 1)
    return offset

def write_order(filename):
    with open(filename, 'w', encoding = "utf-8") as f:
        f.write('focal_points, angle_of_incidence, directions\n')
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
    
