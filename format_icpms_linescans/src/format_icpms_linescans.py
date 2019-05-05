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


def calculate_average(values_list, outlier_index):
    """
    Calculates average and standard deviation taking into account outliers (based on z-score calculation)
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
    numericCounts = [float(i) for i in values_list]
    ave = numpy.mean(numericCounts)
    std = numpy.std(numericCounts)

    return ave, std


def calculate_stats(working_dir, elements):

    with open(os.path.join(working_dir, 'average.csv'), 'w') as w:
        w.write('Element,Line,Average,StdDev,Outliers\n')
        for element in elements:
            symbol = ''.join([char for char in element if not char.isdigit()])
            df = pd.read_csv(os.path.join(working_dir, symbol + '_matrix.csv'), sep=',')
            cols = list(df)
            for col in cols[1:]:
                z = numpy.abs(stats.zscore(df[col]))
                outliers = numpy.where(z > 3)[0]
                ave, std = calculate_average(df[col].tolist(), outliers)
                w.write('{},{},{},{},{}\n'.format(element, col, ave, std, len(outliers)))


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

            sys.exit()







        for directory in dirOnly:
            for spotsize in ['4uM', '15uM', '50uM']:
                dirpath = './' + directory + '/' + spotsize
                outpath = dirpath + '/output'

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

                for k in range(0, len(Smatrix[0])):
                    g1.write("%s,%s,%s,%s,%s,%s\n" % (
                    timepoints[0][k], Smatrix[0][k], Smatrix[1][k], Smatrix[2][k], Smatrix[3][k], Smatrix[4][k]))
                    g2.write("%s,%s,%s,%s,%s,%s\n" % (
                    timepoints[0][k], Camatrix[0][k], Camatrix[1][k], Camatrix[2][k], Camatrix[3][k], Camatrix[4][k]))
                    g3.write("%s,%s,%s,%s,%s,%s\n" % (
                    timepoints[0][k], Fematrix[0][k], Fematrix[1][k], Fematrix[2][k], Fematrix[3][k], Fematrix[4][k]))
                    g4.write("%s,%s,%s,%s,%s,%s\n" % (
                    timepoints[0][k], Znmatrix[0][k], Znmatrix[1][k], Znmatrix[2][k], Znmatrix[3][k], Znmatrix[4][k]))
                    g5.write("%s,%s,%s,%s,%s,%s\n" % (
                    timepoints[0][k], Wmatrix[0][k], Wmatrix[1][k], Wmatrix[2][k], Wmatrix[3][k], Wmatrix[4][k]))

                averagePath = outpath + "/average.csv"
                j = open(averagePath, 'wb')
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

                j.write('S,%.3f,%.3f\n' % (aveStdS[0], aveStdS[1]))
                j.write('Ca,%.3f,%.3f\n' % (aveStdCa[0], aveStdCa[1]))
                j.write('Fe,%.3f,%.3f\n' % (aveStdFe[0], aveStdFe[1]))
                j.write('Zn,%.3f,%.3f\n' % (aveStdZn[0], aveStdZn[1]))
                j.write('W,%.3f,%.3f\n' % (aveStdW[0], aveStdW[1]))

            g1.close()
            g2.close()
            g3.close()
            g4.close()
            g5.close()
            j.close()


if __name__ == '__main__':
    main()
