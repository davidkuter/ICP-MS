# ICP-MS
Collection of Scripts to format data obtained from laser ablation ICP-MS experiments and to visualize it in Matlab

----------------------------------------------------------------------------------------------------------------------------------
Contents:
----------------------------------------------------------------------------------------------------------------------------------

1. format_icpms_map_data
2. Matlab-scripts

----------------------------------------------------------------------------------------------------------------------------------
Descriptions:
----------------------------------------------------------------------------------------------------------------------------------

1: format_icpms_map_data

This folder contains the script used to format the raw 2D map data obtained from laser ablation ICP-MS experiments such that they can then be visualized as contour plots in Matlab. Only csv files are considered. Example data and output is provided.

Installation:
1. Clone the git repo to a location of your choice (`git clone https://github.com/davidkuter/ICP-MS`)
2. CD into the `format_icpms_map_data` folder
3. `pip install -r requirements.txt`
4. `pip install -e .`

Usage: 

`format_icpms_map_data <path_to_data_folder> <x_step_size> <y_step_size>`

2: Matlab-scripts

This folder contains two scripts that are run sequentially to plot laser ablation ICP-MS data in Matlab. The first is "importicpdata.m" which prompts the user to select an element to visualize. Following this, the selected data file is loaded and a frequency distribution is computed to be used to determine upper and lower plot limits. The second script "ploticpdata.m" is then run which prompts the user to select upper and lower limits (which is obtained by looking at the frequency distribution) as well as the number of contour lines wanted. The data is then plot in a new figure.


