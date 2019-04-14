# ICP-MS
Collection of Scripts to format data obtained from laser ablation ICP-MS experiments and to visualize it in Matlab

----------------------------------------------------------------------------------------------------------------------------------
Contents:
----------------------------------------------------------------------------------------------------------------------------------

1. Formatdata
2. Matlab-scripts

----------------------------------------------------------------------------------------------------------------------------------
Descriptions:
----------------------------------------------------------------------------------------------------------------------------------

1. Formatdata

This folder contains the script used to format the raw data obtained from laser ablation ICP-MS experiments such that they can then be visualized by Matlab. Only csv files are considered. Example data and output is provided.

Usage: 

`python format_data.py <path_to_data_folder>`

2. Matlab-scripts

This folder contains two scripts that are run sequentially to plot laser ablation ICP-MS data in Matlab. The first is "importicpdata.m" which prompts the user to select an element to visualize. Following this, the selected data file is loaded and a frequency distribution is computed to be used to determine upper and lower plot limits. The second script "ploticpdata.m" is then run which prompts the user to select upper and lower limits (which is obtained by looking at the frequency distribution) as well as the number of contour lines wanted. The data is then plot in a new figure.


