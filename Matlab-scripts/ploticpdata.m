% Determining limits and contour levels
lowerlimit = input('Enter lower limit for data (look at "histodata"):');              
upperlimit = input('Enter upper limit for data (look at "histodata"):');
contnum = input('Enter number of contour levels you want:');

continterval = (upperlimit - lowerlimit) ./ (contnum - 1);
a = lowerlimit:continterval:upperlimit;
contourlev = transpose(a);
clear a contnum upperlimit lowerlimit continterval

% Plotting figure
figure
contourf(x,y,datafile,contourlev,'edgecolor','none')
title(strcat("LA-ICP-MS plot of ",e));
colormap(jet)
colorbar
axis equal

% Cleaning up unnecessary variables
clear continterval contourlev;
