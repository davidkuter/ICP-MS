import numpy
import pandas as pd
import os
from scipy import stats
import sys


def input_validation(input_args):
    """
    Validates input arguments
    :param input_args: list of arguments of type: ['format_icpms_linescans.py', 'path_to_data_folder']
    :return: False if not valid, else True is returned
    """
    # Determine if number of arguments are correct
    if len(input_args) != 2:
        print("Invalid number of arguments. Usage:")
        print("format_icpms_linescans <path_to_data_folder>")
        return False

    # Determine if directory specified exists
    if not os.path.isdir(input_args[1]):
        print('Directory "{}" does not exist'.format(input_args[1]))
        return False

    return True


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


def file_len(fname):
    """
    Determine length of file
    :param fname: str, path to file
    :return: int, number of lines in file
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def store_data_in_df(csv_files):
    linescan_count = 0
    first_file = True
    df = None
    for csv in csv_files:
        linescan_count += 1

        # If first file, dataframe does not exist yet
        if first_file:
            df = pd.read_csv(csv, sep=',', skiprows=[0, 1, 2])
            df.dropna(inplace=True)
            df['line'] = str(linescan_count)
            first_file = False
        # If dataframe already exists
        else:
            df_next = pd.read_csv(csv, sep=',', skiprows=[0, 1, 2])
            df_next.dropna(inplace=True)
            df_next['line'] = str(linescan_count)
            df = pd.concat([df, df_next])
            del df_next

    return df


def write_all_results(df, working_dir, elements):
    """
    Writes element data from all csv files into a separate results files
    :param df: dataframe, Pandas dataframe containing results from all linescans
    :param working_dir: str, path to current working directory
    :param elements: list, list of elements (for header)
    """

    linescans = df.line.unique().tolist()

    for element in elements:
        # Create symbolic file name from element header
        symbol = ''.join([char for char in element if not char.isdigit()])
        filename = symbol + '_matrix'
        output_file = os.path.join(working_dir, filename + '.csv')

        df_element = df['Time [Sec]'].to_frame()

        for line in linescans:
            # Grab data from each linescan separately for a specific element
            df_matrix = df[element][(df['line'] == str(line))].to_frame()
            new_col = 'line_' + str(line)
            df_matrix.rename(columns={element: new_col}, inplace=True)
            # Create matrix of linescans (columns) vs time
            df_element = df_element.join(df_matrix)
            df_element.drop_duplicates(subset=df_element.columns.difference(['Time [Sec]']), inplace=True)
            del df_matrix

        # write data to file
        df_element.to_csv(output_file, sep=',', index=False)
        print('    Data for {} written to {}'.format(symbol, output_file))


def calc_mod_zscore(values_list):
    """
    Calculates modified Z-score
    (see https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm)
    :param values_list: list, values to calculate the modified Z-score for
    :return: list, Modified Z-scores
    """
    median = numpy.median(values_list)
    abs_dev = [abs(value - median) for value in values_list]
    median_abs_dev = numpy.median(abs_dev)
    return [0.6745*(value - median)/median_abs_dev for value in values_list]


def calculate_average(values_list, outlier_index):
    """
    Calculates average and standard deviation taking into account outliers (based on modified z-score calculation).
    Cutoff of 3.5 is used
    :param values_list: list, List of element counts
    :param outlier_index: list, List of indexes of outlying values that must not be used in the average calculation
    :return: (float, float), Average and standard deviation
    """

    # Remove outliers from list
    if len(outlier_index) != 0:
        outlier_index = sorted(outlier_index, reverse=True)
        for index in outlier_index:
            values_list.pop(int(index))

    # Calculate average and standard deviation
    numeric_counts = [float(i) for i in values_list]
    ave = numpy.mean(numeric_counts)
    std = numpy.std(numeric_counts)

    return ave, std


def calculate_stats(working_dir, elements):
    """
    Calculates outliers (based on z-score) and ave/stdev per line per element
    :param working_dir: str, Location of output folder
    :param elements: list, List of elements to perform calculations on
    """

    with open(os.path.join(working_dir, 'average.csv'), 'w') as w:
        w.write('Element,Line,Average,StdDev,Outliers\n')
        for element in elements:
            symbol = ''.join([char for char in element if not char.isdigit()])
            df = pd.read_csv(os.path.join(working_dir, symbol + '_matrix.csv'), sep=',')
            cols = list(df)
            element_stats = []
            for col in cols[1:]:
                # Determines z-score of data points per line
                z_scores = calc_mod_zscore(df[col])
                # Lists values that have a z-score of > 3.5
                outliers = [x[0] for x in enumerate(z_scores) if x[1] > 3.5]
                # Calculates ave and stdev of non-outlier data per line
                ave, std = calculate_average(df[col].tolist(), outliers)
                element_stats.append(ave)
                # Writes data to file
                w.write('{},{},{},{},{}\n'.format(element, col, ave, std, len(outliers)))
            total_ave = numpy.mean(element_stats)
            total_std = numpy.std(element_stats)
            w.write('{},{},{},{}\n'.format(element, 'Total', total_ave, total_std))


def main():
    valid_input = input_validation(input_args=sys.argv)

    if not valid_input:
        sys.exit()
    else:
        work_path = os.path.abspath(sys.argv[1])

        # Determine spotsize folders
        sub_directories = [x[1] for x in os.walk(work_path)]
        for spotsize in sub_directories[0]:
            spotsize_path = os.path.join(work_path, spotsize)
            print("Formating results in folder: {}".format(spotsize_path))
            out_path = os.path.join(spotsize_path, 'output')
            if not os.path.isdir(out_path):
                os.mkdir(out_path)

            # Determines csv files with the spotsize folder
            print("    Sorting csv files numerically")
            csv_files = [csv_file for csv_file in os.listdir(spotsize_path) if csv_file.endswith(".csv")]
            sorted_csv_files = sorted(csv_files, key=numeric_filename)
            sorted_csv_files = [os.path.join(spotsize_path, text_file) for text_file in sorted_csv_files]

            # Determine elements measured
            print("    Determining elements")
            elements = element_determination(sorted_csv_files[0])

            # Write element data into separate files
            print("    Writing results to separate element files")
            results_df = store_data_in_df(sorted_csv_files)
            write_all_results(results_df, out_path, elements)

            # Determining statistics
            print("    Determining statistics")
            calculate_stats(out_path, elements)


if __name__ == '__main__':
    main()
