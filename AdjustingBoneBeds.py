#!/bin/python3
import math
import argparse

parser = argparse.ArgumentParser(description = "rawtocsv")
parser.add_argument("filename",help = "filenametoparse")
args = parser.parse_args()
Data = open(args.filename, "r")
print("Type of args.filename is: " + str(type(args.filename)))
print("Value of args.filename is: " + args.filename)
NewFile = open(args.filename + ".csv", "w")

Adjustment = .431

for line in Data:
    if line.split(',')[0]=="LS":
        instrumentheight = (float((line.split(',')[1].strip('HI'))))
        rodheight = (float((line.split(',')[2].strip('HR'))))
        print("The instrument height is " + str(instrumentheight) + ".  The rod height is " + str(rodheight) + ".")
    if line.split(',')[0]=="SP":
        Northing = (float((line.split(',')[2].strip('N ')))) + Adjustment
        Easting = (float((line.split(',')[3].strip('E ')))) - Adjustment
        Elevation = (float((line.split(',')[4].strip('EL'))))
        PointName = (str((line.split(',')[1].strip('PN'))))        
        NewFile.write(str(Northing) + ',' + str(Easting) + ',' + str(Elevation) + ',' + str(PointName) + "\n")
        
Data.close()
