import os
import pandas as pd
import sys


def input_validation(input_args):
    """
    Validates input arguments
    :param input_args: list of arguments of type: ['format_data.py', 'path_to_data_folder', 'x_step', 'y_step']
    :return: False if not valid, else True is returned
    """
    # Determine if number of arguments are correct
    if len(input_args) != 4:
        print("Invalid number of arguments. Usage:")
        print("format_data.py <path_to_data_folder> <x_step_size> <y_step_size")
        return False

    # Determine if step sizes provided are valid
    try:
        float(input_args[2])
        float(input_args[3])
    except ValueError:
        print('X and/or Y step size ("{}" and/or "{}") is not a valid number'.format(input_args[2], input_args[3]))
        return False

    # Determine if directory specified exists
    if not os.path.isdir(input_args[1]):
        print('Directory "{}" does not exist'.format(input_args[1]))
        return False

    return True


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


def write_all_results(output_path, file_list, element_list, x_step, y_step):
    """
    Writes results from all csv files into a single summary file
    :param output_path: str, full path to output file that is to be created
    :param file_list: list, list of files (full path) to extract data from
    :param element_list: list, list of elements (only needed for header creation)
    :param x_step: float, step size in x direction
    :param y-step: float, step size in y direction
    :return: results csv file, x and y csv file
    """
    x_file_path = os.path.join(work_path, 'output/x_data.csv')
    y_file_path = os.path.join(work_path, 'output/y_data.csv')

    x_list = []
    y_list = []
    with open(output_path, 'w') as g:
        g.write("x,y,{}\n".format(','.join(element_list)))
        y = 0

        for csv_file in file_list:
            # Establish Y step per file and reset X step. Create a list of unique Y-values to write to file later
            x = 0
            y = y + y_step
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
                        x = x + x_step
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
        e_path = os.path.join(work_path, e_file_name)

    with open(e_path, 'w') as W:
        unique_y = df.y.unique().tolist()
        for y in unique_y:
            df_selected = df[df['y'] == y]
            values_list = df_selected[header[0]].tolist()
            values_list = [str(value) for value in values_list]
            W.write("{}\n".format(','.join(values_list)))


# Main script
valid_input = input_validation(input_args=sys.argv)

if not valid_input:
    sys.exit()
else:
    # Store input arguments into variables
    x_step_size = float(sys.argv[2])
    y_step_size = float(sys.argv[3])
    work_path = os.path.abspath(sys.argv[1])
    if not os.path.isdir(os.path.join(work_path, 'output')):
        os.mkdir(os.path.join(work_path, 'output'))
    print('Processing data in: {}'.format(work_path))
    print('Step size in x direction: {}'.format(str(x_step_size)))
    print('Step size in y direction: {}'.format(str(y_step_size)))

    # Find all csv files in folder, sort by the numerical component and store in list with their full path
    # https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052
    # https://stackoverflow.com/questions/37796598/how-to-sort-file-names-in-a-particular-order-using-python
    filenames = os.listdir(work_path)
    file_list = [filename for filename in filenames if filename.endswith(".csv")]
    textfiles = sorted(file_list, key=numeric_filename)
    textfiles = [os.path.join(work_path, textfile) for textfile in textfiles]

    # Determine elements measured
    elements = element_determination(textfiles[0])

    # Create one file to store all results
    outfile = os.path.join(work_path, 'output/alldata.csv')
    write_all_results(output_path=outfile, file_list=textfiles, element_list=elements,
                      x_step=x_step_size, y_step=y_step_size)

    # Parse results file to create individual matrix files
    df = pd.read_csv(outfile, sep=',')
    for element in elements:
        df_element = df[['x', 'y', element]]
        create_element_matrices(df=df_element)
