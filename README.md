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
│   └───gcodes
│   └───orders
```

## USAGE:

```sh
python3 generate_gcode.py -idx <user index> -a <pointA coordinate(x,y)> -b <pointB coordinate(x,y)> -c <pointC coordinate(x,y)> -d <pointD coordinate(x,y)> -e <pointE coordinate(x,y)>
```
	
For example,
if you want to generate the gcode file for user #6, 
under scripts directory, run

```sh
python3 generate_gcode.py -idx 6 -a 50 60 -b 40 50 -c 50 40 -d 60 50 -e 50 50
```

#### Note: fill in the coordinate fields with the exact positions of the five focal points you measured earlier.
#### Note: you can change the suffix for the output file by args '-gcode_out' and '-order_out'.

## OTHER NOTICES:

- the order is randomized using the user index as the random seed, so that the result stays the same for each user everytime you run the program.
- the printer only moves when the focal points change. That is to say, there can be more than one sample to collect during one pause action. The details of the samples will be shown in the log in 86duino repetier host. The log is used to indicate the adjustments for the directions and angles of the motors.
