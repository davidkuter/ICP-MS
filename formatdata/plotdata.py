#######################################################################
# November 2017 - David Kuter                                         #
#                                                                     #
# Script to extract counts from LA-ICP-MS data (SMPL.csv files)       #
# This script requires the "sortcsv.sh" bash script in order to run   #
# correctly since it is used to numerically order the csv files.      #
#######################################################################

import glob, os
import sys 
from subprocess import call

#######################################################################
########                       Variables                        #######
#######################################################################
xstepsize = 0.01
ystepsize = 0.01

#######################################################################
########                       Definitions                      #######
#######################################################################
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#######################################################################
########                       Main Script                      #######
#######################################################################

if not os.path.isdir('./output'):
    os.mkdir('./output')

if not os.path.isfile('sortcsv.sh'):
    print ("Please ensure sortcsv.sh is present in the directory!")
    exit()

call("./sortcsv.sh")

textfiles = []

with open('textfiles.tmp') as t:
    for linet in t:
        textfiles.append(linet)
        textfiles[-1] = textfiles[-1].strip()

g = open('./output/alldata.csv', 'wb')         
g1 = open('./output/P_matrix.csv', 'wb')         
g2 = open('./output/Ca_matrix.csv', 'wb')         
g3 = open('./output/Fe_matrix.csv', 'wb')         
g4 = open('./output/Zn_matrix.csv', 'wb')         
g5 = open('./output/W_matrix.csv', 'wb')         
gx = open('./output/x_data.csv', 'wb')         
gy = open('./output/y_data.csv', 'wb')         

x = 0
y = 0
xstep = xstepsize
ystep = ystepsize
         
g.write("x,y,P,Ca,Fe,Zn,W\n")

firstfile = 0

for i in textfiles:
   
    counter = 0
    firstfile = firstfile + 1
 
    with open(i) as f:
        
         filelen = file_len(i)     
         footer = filelen - 3

         x = 0         
         y = y + ystep
         gy.write("%.2f\n" % y)

         P = []
         Ca = []
         Fe = []
         Zn = []
         W = []

         for line in f:
          
             a = []   
             counter = counter + 1

             if 5 <= counter <= footer:
                
                  x = x + xstep            

                  if firstfile == 1:
                      gx.write("%.2f\n" % x)

                  a = line.split(',')
                  a[-1] = a[-1].strip()

                  g.write( "%.2f,%.2f,%s,%s,%s,%s,%s\n" % (x, y, a[1], a[2], a[3], a[4], a[5]) )

                  P.append(a[1])
                  Ca.append(a[2])
                  Fe.append(a[3])
                  Zn.append(a[4])
                  W.append(a[5])
             

         listlen = len(W)

         for j in range(0,listlen):

             if j == 0:
                 g1.write( "%s" % P[j] )  
                 g2.write( "%s" % Ca[j] )  
                 g3.write( "%s" % Fe[j] )  
                 g4.write( "%s" % Zn[j] )  
                 g5.write( "%s" % W[j] )  
             else:
                 g1.write( ",%s" % P[j] )  
                 g2.write( ",%s" % Ca[j] )  
                 g3.write( ",%s" % Fe[j] )  
                 g4.write( ",%s" % Zn[j] )  
                 g5.write( ",%s" % W[j] )  

         g1.write( "\n" )
         g2.write( "\n" )
         g3.write( "\n" )
         g4.write( "\n" )
         g5.write( "\n" )
   
   
 



