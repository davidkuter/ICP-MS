import os
import pandas as pd
import sys

# Global Variables
XSTEPSIZE = 0.015
YSTEPSIZE = 0.015


def file_len(fname):
    """
    Determines number of rows (length) in file
    :param fname: str, name of file
    :return: int, number of rows in file
    """
    with open(fname) as F:
        for row_num, row_content in enumerate(F):
            pass
    return row_num + 1


def numeric_filename(filename):
    """
    Determines the numeric portion of a filename. E.g. 0123SMPL.csv => 0123
    :param filename: str, name of a file
    :return: int, numeric portion of filename
    """
    return filename[:3]


def element_determination(sample_file):
    """
    Determines the elements measured in a file
    :param sample_file: str, filename
    :return: list of elements
    """
    with open(sample_file) as F:
        # Skips unnecessary header
        for skip in range(0, 3):
            next(F)
        element_header = F.readline()
    return element_header.strip().split(',')[1:]


def write_all_results(output_path, file_list, element_list):
    """
    Writes results from all csv files into a single summary file
    :param output_path: str, full path to output file that is to be created
    :param file_list: list, list of files (full path) to extract data from
    :param element_list: list, list of elements (only needed for header creation)
    :return: results csv file, x and y csv file
    """
    x_file_path = os.path.join(WORK_PATH, 'output/x_data.csv')
    y_file_path = os.path.join(WORK_PATH, 'output/y_data.csv')

    x_list = []
    y_list = []
    with open(output_path, 'w') as g:
        g.write("x,y,{}\n".format(','.join(element_list)))
        y = 0

        for csv_file in file_list:
            # Establish Y step per file and reset X step. Create a list of unique Y-values to write to file later
            x = 0
            y = y + YSTEPSIZE
            if y not in y_list:
                y_list.append(y)

            # Read data from file and store in a list. Line counter is required to skip header and footer info.
            line_counter = 0
            footer = file_len(csv_file) - 3
            with open(csv_file, 'r') as R:
                for line in R:
                    line_counter += 1
                    if 5 <= line_counter <= footer:
                        # Establish X step per row in file. Create a list of unique values to write to file later
                        x = x + XSTEPSIZE
                        if x not in x_list:
                            x_list.append(x)

                        # Extract required data and write to results file
                        line = line.strip().split(',')
                        g.write("{},{},{}\n".format(x, y, ','.join(line[1:])))

    # Write out X and Y steps
    with open(x_file_path, 'w') as gx, open(y_file_path, 'w') as gy:
        x_list = [str(x) for x in x_list]
        y_list = [str(y) for y in y_list]
        gx.write('\n'.join(x_list))
        gy.write('\n'.join(y_list))


def create_element_matrices(df):
    """
    Reads dataframe consisting of x & y positions and element counts. Reformats data into matrix format.
    :param df: dataframe
    :return: element matrix csv file
    """
    # Create element file to write to
    header = list(df.columns.values)
    header.remove('x')
    header.remove('y')
    if len(header) != 1:
        return
    else:
        e = ''.join([i for i in header[0] if not i.isdigit()])
        e_file_name = "output/" + e + "_matrix.csv"
        e_path = os.path.join(WORK_PATH, e_file_name)

    with open(e_path, 'w') as W:
        unique_y = df.y.unique().tolist()
        for y in unique_y:
            df_selected = df[df['y'] == y]
            values_list = df_selected[header[0]].tolist()
            values_list = [str(value) for value in values_list]
            W.write("{}\n".format(','.join(values_list)))


# Main script
if len(sys.argv) != 2:
    print("Invalid number of arguments. Usage:")
    print("format_data.py <path_to_data_folder>")
    sys.exit()
else:
    # Determine if directory specified exists
    if not os.path.isdir(sys.argv[1]):
        print("Directory {} does not exist".format(sys.argv[1]))
        sys.exit()
    else:
        WORK_PATH = os.path.abspath(sys.argv[1])
        if not os.path.isdir(os.path.join(WORK_PATH, 'output')):
            os.mkdir(os.path.join(WORK_PATH, 'output'))

    # Find all csv files in folder, sort by the numerical component and store in list with their full path
    # https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052
    # https://stackoverflow.com/questions/37796598/how-to-sort-file-names-in-a-particular-order-using-python
    filenames = os.listdir(WORK_PATH)
    file_list = [filename for filename in filenames if filename.endswith(".csv")]
    textfiles = sorted(file_list, key=numeric_filename)
    textfiles = [os.path.join(WORK_PATH, textfile) for textfile in textfiles]

    # Determine elements measured
    elements = element_determination(textfiles[0])

    # Create one file to store all results
    outfile = os.path.join(WORK_PATH, 'output/alldata.csv')
    write_all_results(output_path=outfile, file_list=textfiles, element_list=elements)

    # Parse results file to create individual matrix files
    df = pd.read_csv(outfile, sep=',')
    for element in elements:
        df_element = df[['x', 'y', element]]
        create_element_matrices(df=df_element)

#g = open('./output/alldata.csv', 'w')
#g1 = open('./output/P_matrix.csv', 'w')
#g2 = open('./output/Ca_matrix.csv', 'w')
#g3 = open('./output/Fe_matrix.csv', 'w')
#g4 = open('./output/Zn_matrix.csv', 'w')
#g5 = open('./output/W_matrix.csv', 'w')
#gx = open('./output/x_data.csv', 'w')
#gy = open('./output/y_data.csv', 'w')

#x = 0
#y = 0
#xstep = XSTEPSIZE
#ystep = YSTEPSIZE
         
#g.write("x,y,P,Ca,Fe,Zn,W\n")

#firstfile = 0

#for i in textfiles:
#    counter = 0
#    firstfile = firstfile + 1
 
#    with open(i) as f:
        
#         filelen = file_len(i)
#         footer = filelen - 3

#         x = 0
#         y = y + ystep
#         gy.write("%.2f\n" % y)

#         P = []
#         Ca = []
#         Fe = []
#         Zn = []
#         W = []

#         for line in f:
          
#             a = []
#             counter = counter + 1

#             if 5 <= counter <= footer:
                
#                  x = x + xstep

#                  if firstfile == 1:
#                      gx.write("%.2f\n" % x)

#                  a = line.split(',')
#                  a[-1] = a[-1].strip()

#                  g.write("%.2f,%.2f,%s,%s,%s,%s,%s\n" % (x, y, a[1], a[2], a[3], a[4], a[5]))

#                  P.append(a[1])
#                  Ca.append(a[2])
#                  Fe.append(a[3])
#                  Zn.append(a[4])
#                  W.append(a[5])

#         listlen = len(W)

#         for j in range(0, listlen):

#             if j == 0:
#                 g1.write( "%s" % P[j] )
#                 g2.write( "%s" % Ca[j] )
#                 g3.write( "%s" % Fe[j] )
#                 g4.write( "%s" % Zn[j] )
#                 g5.write( "%s" % W[j] )
#             else:
#                 g1.write( ",%s" % P[j] )
#                 g2.write( ",%s" % Ca[j] )
#                 g3.write( ",%s" % Fe[j] )
#                 g4.write( ",%s" % Zn[j] )
#                 g5.write( ",%s" % W[j] )

#         g1.write( "\n" )
#         g2.write( "\n" )
#         g3.write( "\n" )
#         g4.write( "\n" )
#         g5.write( "\n" )
   
   
 



