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

2. Matlab-scripts

This folder contains two scripts that are run sequentially to plot laser ablation ICP-MS data in Matlab. The first is "importicpdata.m" which prompts the user to select an element to visualize. Following this, the selected data file is loaded and a frequency distribution is computed to be used to determine upper and lower plot limits. The second script "ploticpdata.m" is then run which prompts the user to select upper and lower limits (which is obtained by looking at the frequency distribution) as well as the number of contour lines wanted. The data is then plot in a new figure.


