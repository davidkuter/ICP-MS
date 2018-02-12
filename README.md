# ICP-MS
Collection of Scripts to format data obtained from laser ablation ICP-MS experiments and to visualize it in Matlab

----------------------------------------------------------------------------------------------------------------------------------
Contents:
----------------------------------------------------------------------------------------------------------------------------------

1. Formatdata

----------------------------------------------------------------------------------------------------------------------------------
Descriptions:
----------------------------------------------------------------------------------------------------------------------------------

1. Formatdata

This folder contains the script used to format the raw data obtained from laser ablation ICP-MS experiments such that they can then be visualized by Matlab. The python script "plotdata.py" (badly named since it does not actually plot data just provides the data so as to enable subsequently plotting - hence the folder is called format data) must be run in the directory containing the individual line scan data (csv files) and MUST also have the sortcsv.sh bash script in the same folder to properly run. The reason for this is that the bash script is called to sort csv files numerically. I wrote it in this way because doing this in python seemed unnecessarily complicated. In hind sight, I can probably do a better job of this now and may implement an internal sorting procedure at a later stage. For now, just make sure it is there.



