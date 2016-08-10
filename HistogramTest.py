#!/bin/python3
import ROOT
import ROOT.Math
import math
import argparse

parser = argparse.ArgumentParser(description = "rawtocsv")
parser.add_argument("filename",help = "filenametoparse")
args = parser.parse_args()
Data = open(args.filename, "r")
instrumentheight = 0
rodheight = 0

MAKE_THE_Y_AXIS_THE_X_AXIS = 90

CONVERSION_FOR_BACKSITE_TO_Y_AXIS = 28 

canvas = ROOT.TCanvas("c", "Graph2Dexample", 0, 0, 700, 600)
 
graph = ROOT.TGraph2D()

# N variable used to incrementthe graph.SetPoint
N = 0
csvdictionary = {}

for line in Data:
    if line.split(',')[0]=="LS":
        instrumentheight = (float((line.split(',')[1].strip('HI'))))
        rodheight = (float((line.split(',')[2].strip('HR'))))
        print("The instrument height is " + str(instrumentheight) + ".  The rod height is " + str(rodheight) + ".")
    if line.split(',')[0] == "SS":
        zenith = (float((line.split(',')[4].strip('ZE' ))))
        azimuth = (float((line.split(',')[3].strip('AR' ))))
        hypotenuse = (float((line.split(',')[5].strip('SD' ))))
        description = (((line.split(',')[6].strip('--').strip('\n'))))
        
        if description not in csvdictionary:
            csvdictionary[description] = open(args.filename.strip(".raw") + "_" + description + ".csv", "w")        

        nexttest = ROOT.Math.Polar3DPoint(hypotenuse, math.radians(zenith), math.radians(360 - azimuth + CONVERSION_FOR_BACKSITE_TO_Y_AXIS + MAKE_THE_Y_AXIS_THE_X_AXIS))
        pointz = (nexttest.Z() - rodheight + instrumentheight)
        print("The Zenith is "+ str(zenith) + ".  The Azimuth is " + str(azimuth) + ".  The Hypotenuse is " + str(hypotenuse) + ". The description is " + str(description) + ".  The X, Y and Z are " + str(nexttest.X()) + str(nexttest.Y()) + str(pointz) + ".")
        csvdictionary[description].write(str(nexttest.X())+ "," + str(nexttest.Y()) + "," + str(pointz)+ "\n" ) 
        graph.SetPoint(N, nexttest.X(), nexttest.Y(), pointz)  
        N = N + 1

for filehandle in csvdictionary:
    csvdictionary[filehandle].close()

Data.close()
graph.GetXaxis().SetCanExtend(False)
graph.GetZaxis().SetLimits(-1.5,-2.5)
graph.Draw("TRI1")
canvas.Update()
canvas.Draw("TRI1")

input()
