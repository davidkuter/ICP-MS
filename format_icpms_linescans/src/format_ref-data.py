#######################################################################
# April 2018 - David Kuter                                            #
#                                                                     #
# Script to extract counts from LA-ICP-MS data (SMPL.csv files)       #
# of reference samples with different spot sizes                      #
# This script requires the "sortcsv.sh" bash script in order to run   #
# correctly since it is used to numerically order the csv files.      #
#######################################################################

import glob, os
import sys
import numpy 
from subprocess import call

#######################################################################
########                       Definitions                      #######
#######################################################################
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def aveOnly(counts):
  
    del counts[0]
    numericCounts = [float(i) for i in counts]
 
    ave = numpy.mean(numericCounts)

    return ave  
     
def aveStd(counts):
    ave = numpy.mean(counts)
    std = numpy.std(counts)

    b = []
    b.append(ave)
    b.append(std)

    return b  

#######################################################################
########                       Main Script                      #######
#######################################################################

allfiles = os.listdir('.')

dirOnly = []

for filename in allfiles:
    if os.path.isdir(os.path.join(os.path.abspath("."), filename)):
        dirOnly.append(filename)

dirOnly.sort()

for directory in dirOnly:
    for spotsize in ['4uM','15uM','50uM']:
        dirpath = './' + directory + '/' + spotsize
        outpath = dirpath + '/output'

        if not os.path.isdir(outpath): os.mkdir(outpath)

        csvfiles = []
        for subfile in os.listdir(dirpath):
            if subfile.endswith(".csv"): csvfiles.append(subfile)

        SmatrixPath = outpath + "/S_matrix.csv"
        CamatrixPath = outpath + "/Ca_matrix.csv"
        FematrixPath = outpath + "/Fe_matrix.csv"
        ZnmatrixPath = outpath + "/Zn_matrix.csv"
        WmatrixPath = outpath + "/W_matrix.csv"
        g1 = open(SmatrixPath, 'wb')         
        g2 = open(CamatrixPath, 'wb')         
        g3 = open(FematrixPath, 'wb')         
        g4 = open(ZnmatrixPath, 'wb')         
        g5 = open(WmatrixPath, 'wb')         

        timepoints = []
        Smatrix = []
        Camatrix = []
        Fematrix = []
        Znmatrix = []
        Wmatrix = []
        

        for i in csvfiles:

            opendir = dirpath + "/" + i

            counter = 0

            with open(opendir) as f:
                filelen = file_len(opendir)     
                footer = filelen - 3

                time = []
                S = []
                Ca = []
                Fe = []
                Zn = []
                W = []

                for line in f:

                    counter = counter + 1
                    a = []

                    if 5 <= counter <= footer:

                        a = line.split(',')
                        a[-1] = a[-1].strip()
            

                        time.append(a[0])
                        S.append(a[1])
                        Ca.append(a[2])
                        Fe.append(a[3])
                        Zn.append(a[4])
                        W.append(a[5])
                
            timepoints.append(time)
            Smatrix.append(S)     
            Camatrix.append(Ca)     
            Fematrix.append(Fe)     
            Znmatrix.append(Zn)     
            Wmatrix.append(W) 

            f.close()


        for k in range(0,len(Smatrix[0])):

           g1.write("%s,%s,%s,%s,%s,%s\n" % (timepoints[0][k], Smatrix[0][k], Smatrix[1][k], Smatrix[2][k], Smatrix[3][k], Smatrix[4][k]) ) 
           g2.write("%s,%s,%s,%s,%s,%s\n" % (timepoints[0][k], Camatrix[0][k], Camatrix[1][k], Camatrix[2][k], Camatrix[3][k], Camatrix[4][k]) ) 
           g3.write("%s,%s,%s,%s,%s,%s\n" % (timepoints[0][k], Fematrix[0][k], Fematrix[1][k], Fematrix[2][k], Fematrix[3][k], Fematrix[4][k]) ) 
           g4.write("%s,%s,%s,%s,%s,%s\n" % (timepoints[0][k], Znmatrix[0][k], Znmatrix[1][k], Znmatrix[2][k], Znmatrix[3][k], Znmatrix[4][k]) ) 
           g5.write("%s,%s,%s,%s,%s,%s\n" % (timepoints[0][k], Wmatrix[0][k], Wmatrix[1][k], Wmatrix[2][k], Wmatrix[3][k], Wmatrix[4][k]) ) 

        averagePath = outpath + "/average.csv"
        j = open(averagePath,'wb')
        j.write('element,average,std\n')

        lineAveS = []
        lineAveCa = []
        lineAveFe = []
        lineAveZn = []
        lineAveW = []

        for lineS in Smatrix: 
            ave = aveOnly(lineS) 
            lineAveS.append(ave)

        for lineCa in Camatrix: 
            ave = aveOnly(lineCa) 
            lineAveCa.append(ave)

        for lineFe in Fematrix: 
            ave = aveOnly(lineFe) 
            lineAveFe.append(ave)

        for lineZn in Znmatrix: 
            ave = aveOnly(lineZn) 
            lineAveZn.append(ave)

        for lineW in Wmatrix: 
            ave = aveOnly(lineW) 
            lineAveW.append(ave)

        aveStdS = aveStd(lineAveS)
        aveStdCa = aveStd(lineAveCa)
        aveStdFe = aveStd(lineAveFe)
        aveStdZn = aveStd(lineAveZn)
        aveStdW = aveStd(lineAveW)
 
        j.write('S,%.3f,%.3f\n' % (aveStdS[0],aveStdS[1]) )
        j.write('Ca,%.3f,%.3f\n' % (aveStdCa[0],aveStdCa[1]) )
        j.write('Fe,%.3f,%.3f\n' % (aveStdFe[0],aveStdFe[1]) )
        j.write('Zn,%.3f,%.3f\n' % (aveStdZn[0],aveStdZn[1]) )
        j.write('W,%.3f,%.3f\n' % (aveStdW[0],aveStdW[1]) )


    g1.close()        
    g2.close()        
    g3.close()        
    g4.close()        
    g5.close()       
    j.close() 



