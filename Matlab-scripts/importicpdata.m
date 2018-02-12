clear
% Importing relevant data files
element = input('Enter element of interest (atomic symbol):','s');
e = upper(element);

if e == 'CA'                % Assigning atomic symbols to correct data files (must be all-caps)
    datafile = importdata('Ca_matrix.csv');
elseif e == 'FE' 
    datafile = importdata('Fe_matrix.csv');
elseif e == 'P' 
    datafile = importdata('P_matrix.csv');
elseif e == 'W' 
    datafile = importdata('W_matrix.csv');
elseif e == 'ZN' 
    datafile = importdata('Zn_matrix.csv');
else
    disp("Cannot determine element type! Edit script to ensure element file is assigned!")
    return
end

x = importdata('x_data.csv');
y = importdata('y_data.csv');

% Histogram analysis
binnum = input('Enter number of bins you want for the histogram analysis:');
[N,edges]=histcounts(datafile(:),binnum,'Normalization','probability');
histodata = horzcat(transpose(edges(:,1:end-1)),N(:));
histosum = cumsum(histodata(:,2));
histosum = histosum*100;
histodata = horzcat(histodata,histosum);

clear binnum N edges histosum element;

