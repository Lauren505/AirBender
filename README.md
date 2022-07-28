# README

This is a README file for generate_gcode.py

## SYNOPSIS:

This program generates a randomized g-code script for an individual user

## DIRECTORY:

```
AirBender
│   README.md
└───scripts
│   │   generate_gcode.py
│   │   set_servo_angle.py
│   │   uservo.py
│   └───gcodes
│   └───orders
```

## USAGE:

### generate gcode

```sh
python3 generate_gcode.py -idx <user index> -a <pointA coordinate(x,y)> -b <pointB coordinate(x,y)> -c <pointC coordinate(x,y)> -d <pointD coordinate(x,y)> -e <pointE coordinate(x,y)> -angle <angle of incidence>
```

For example,
if you want to generate the gcode file for user #6,
under scripts directory, run

```sh
python3 generate_gcode.py -idx 6 -a 50 60 -b 40 50 -c 50 40 -d 60 50 -e 50 50 -angle 30
```

Fill in the coordinate fields with the exact positions of the five focal points you measured earlier.
You can change the suffix for the output file by args '-gcode_out' and '-order_out'.

### automate servo

Modify the servo port, baud rate, and servo IDs in `set_servo_angle.py`.

```sh
python3 set_servo_angle.py -f <path to file>
```

For example,

```sh
python3 set_servo_angle.py -f ./orders/0_order.txt
```

The program pauses for 10 seconds per sample for the operator to fire the air jet and the user to fill out his/her answer. If the next focal point is different from the current point, then the pause time extends to seconds. You can modify this in line 43 & 45.

### servo_controller.py
Call using python3 servo_controller.py -r x -i y -a z
-r [0,1] to indicate whether or not a previous servo offset must be compensated for (just call this after moving to an angle >= 270)
-i [0,30,60,90] to set the incident angle of the servo
-a [0,15,...,330,345] to set the rotational angle of the servo

## OTHER NOTICES:

- the order is randomized using the user index as the random seed, so that the result stays the same for each user everytime you run the program.
- the printer only moves when the focal points change. That is to say, there can be more than one sample to collect during one pause action. The details of the samples will be shown in the log in 86duino repetier host. The log is used to indicate the adjustments for the directions and angles of the motors.
