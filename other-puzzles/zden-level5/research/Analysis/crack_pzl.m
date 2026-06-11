%% Clear all
clear all;
close all;
clc;

%% Load packages
pkg load statistics

%% Load and prepare the image "map"
    % Load the image
Img = imread('crypto5fix.png');
    % All thrre RGB channels are identical here (1 or 0 value)
    % take only 1 to work with
data = Img(:,:,1);

    % Delete the non-rectangle data
data(780:950,1:140)=0;
data(780:950,770:950)=0;
data(890:950,1:950)=0;

    % honestly dont know exactly why the original type of "data" taste bad 
    % for octave fucntions, but anyway - get the octave what it like
data = real(data);

%% Evaluate the rectangles coordinates and area

    % At first - get the list of coordinates for each rectangle "center
    % (Could be made through some tweaked clusterization, but 
    % hardcoding here is faster and simpler - k-means with L2 and L1 failed
    % anyway)
%        % Take coordinates of all non-zero points for cluster analysis
%[x_vect, y_vect] = ind2sub([size(data,1), size(data,2)],  find(data==1));
%[idx, centers] = kmeans([x_vect, y_vect], 64, 'Distance', 'hamming');

x_y = [125, 215;...
       125, 290;...
       125, 370;...
       125, 445;...
       125, 510;...
       125, 600;...
       123, 670;...
       125, 730;...
       
       223, 240;...
       223, 278;...
       223, 327;...
       223, 400;...
       223, 470;...
       223, 525;...
       223, 578;...
       223, 670;...
     
       322, 247;...
       322, 335;...
       322, 416;...
       322, 489;...
       322, 543;...
       322, 590;...
       322, 650;...
       322, 704;...
     
       420, 192;...
       420, 273;...
       420, 342;...
       420, 403;...
       420, 477;...
       420, 562;...
       420, 640;...
       420, 738;...
     
       522, 245;...
       522, 299;...
       522, 362;...
       522, 417;...
       522, 478;...
       522, 564;...
       522, 632;...
       522, 691;...
     
       623, 274;...
       623, 324;...
       623, 386;...
       623, 454;...
       623, 507;...
       623, 547;...
       623, 588;...
       623, 650;...
     
       720, 230;...
       720, 323;...
       720, 397;...
       720, 490;...
       722, 570;...
       722, 602;...
       722, 642;...
       722, 718;...
     
       822, 243;...
       822, 320;...
       822, 380;...
       822, 450;...
       822, 523;...
       822, 591;...
       822, 648;...
       822, 703 ];

fig1 = imagesc(data);
hold on
scatter(x_y(:,2), x_y(:,1));

    % Then get coordinates of rectangles    
        % x-coordinates
for sqr_idx = 1:64  
    xi_1 = find((data(x_y(sqr_idx, 1), 1:end) ==1) .* ( (1:size(data, 2)) < x_y(sqr_idx, 2)), 1, 'last');
    xi_2 = find((data(x_y(sqr_idx, 1), 1:end) ==1) .* ( (1:size(data, 2)) >= x_y(sqr_idx, 2)), 1, 'first');

    xo_1 = find((data(x_y(sqr_idx, 1), 1:end) ==0) .* ( (1:size(data, 2)) <= xi_1), 1, 'last') + 1;
    xo_2 = find((data(x_y(sqr_idx, 1), 1:end) ==0) .* ( (1:size(data, 2)) >= xi_2), 1, 'first') - 1;

    X(sqr_idx,:) = [xo_1, xi_1, xi_2, xo_2];
end

fig2 = figure;
imagesc(data);
hold on
for sqr_idx = 1:64 
    xo_1 = X(sqr_idx, 1);
    xi_1 = X(sqr_idx, 2);
    xi_2 = X(sqr_idx, 3);
    xo_2 = X(sqr_idx, 4);
    
    scatter(xo_1, x_y(sqr_idx, 1), 'r');
    scatter(xi_1, x_y(sqr_idx, 1), 'g');
    scatter(xi_2, x_y(sqr_idx, 1), 'b');
    scatter(xo_2, x_y(sqr_idx, 1), 'k');
end
title('horizontal coordinates verification');

        % y-coordinates
for sqr_idx = 1:64  
    yi_1 = find( (data( 1:end, x_y(sqr_idx, 2) ) == 1) .* ( (1:size(data, 1)) <  x_y(sqr_idx, 1))',  1, 'last');
    yi_2 = find( (data( 1:end, x_y(sqr_idx, 2) ) == 1) .* ( (1:size(data, 1)) >= x_y(sqr_idx, 1))', 1, 'first');

    yo_1 = find( (data( 1:end, x_y(sqr_idx, 2) ) == 0) .* ( (1:size(data, 1)) <= yi_1)',            1, 'last') + 1;
    yo_2 = find( (data( 1:end, x_y(sqr_idx, 2) ) == 0) .* ( (1:size(data, 1)) >= yi_2)',            1, 'first') - 1;

    Y(sqr_idx,:) = [yo_1, yi_1, yi_2, yo_2];
end

fig3 = figure;
imagesc(data)
hold on
for sqr_idx = 1:64 
    yo_1 = Y(sqr_idx, 1);
    yi_1 = Y(sqr_idx, 2);
    yi_2 = Y(sqr_idx, 3);
    yo_2 = Y(sqr_idx, 4);
    
    scatter(x_y(sqr_idx, 2), yo_1, 'r');
    scatter(x_y(sqr_idx, 2), yi_1, 'g');
    scatter(x_y(sqr_idx, 2), yi_2, 'b');
    scatter(x_y(sqr_idx, 2), yo_2, 'k');
end
title('vertical coordinates verification');

    % Finally, the AREAS ( or else metrics) could be evaluated for rectangels.
    % Lets estimate the area of each outter and inner rectangles
for sqr_idx = 1:64 
    xo_1 = X(sqr_idx, 1);
    xi_1 = X(sqr_idx, 2);
    xi_2 = X(sqr_idx, 3);
    xo_2 = X(sqr_idx, 4);
    
    yo_1 = Y(sqr_idx, 1);
    yi_1 = Y(sqr_idx, 2);
    yi_2 = Y(sqr_idx, 3);
    yo_2 = Y(sqr_idx, 4);
    
    A_o = (abs(xo_1 - xo_2)    + 1) * (abs(yo_1 - yo_2)    + 1);
    A_i = (abs(xi_1 - xi_2) -2 + 1) * (abs(yi_1 - yi_2) -2 + 1);
    
    A(sqr_idx, :) = [A_o, A_i];
end

A(40, 1) = A(40, 1)  * 17;
A(53, 1) = A(53, 1)  *  6; 

%% Try to apply that hint - get 32 bytes

    % In current notation, we have rectangles written in list indecies of which 
    % could be shown on the 8 x 8 original grid as follows:
    %
    %  1   2  3  4  5  6  7  8
    %  9  10 11 12 13 14 15 16
    %  17 18 19 20 21 22 23 24
    %  25 26 27 28 29 30 31 32
    %  33 34 35 36 37 38 39 40
    %  41 42 43 44 45 46 47 48
    %  49 50 51 52 53 54 55 56
    %  57 58 59 60 61 62 63 64
    

    % Assume the author hinted to get sum of RECTANGULAR SHELLS that follows
    % each other from left to right continuesly from the top to the bottom
    % In our indices - 1+2; 3+4; 5+6; 7+8; 9+10; ...; 61+62; 63+64
    
    %....
    
bytes_values = zeros(32, 12);

idx{1} = [((1:32)'-1)*2 + 1, ((1:32)'-1)*2 + 2;];

idx{2} = [[1:8,17:24,33:40,49:56]', [9:16,25:32,41:48,57:64]'];

idx{3} = reshape(reshape(1:64,8,8)',2,[])';

idx{4} = [[1, 9,17,25,33,41,49,57, 3,11,19,27,35,43,51,59, 5,13,21,29,37,45,53,61, 7,15,23,31,39,47,55,63]',...
          [2,10,18,26,34,42,50,58, 4,12,20,28,36,44,52,60, 6,14,22,30,38,46,54,62, 8,16,24,32,40,48,56,64]'];

idea_counter = 1;  
for Iidx = 1:length(idx)  
    for Ib = 1:32
        idx_1 = idx{Iidx}(Ib, 1);
        idx_2 = idx{Iidx}(Ib, 2);
    
        bytes_values(Ib, idea_counter) = A(idx_1, 2) + A(idx_2, 2);    
    end
    idea_counter = idea_counter + 1;
    for Ib = 1:32
        idx_1 = idx{Iidx}(Ib, 1);
        idx_2 = idx{Iidx}(Ib, 2);
    
        bytes_values(Ib, idea_counter) = A(idx_1, 1) + A(idx_2, 1);    
    end
    idea_counter = idea_counter + 1;    
    for Ib = 1:32
        idx_1 = idx{Iidx}(Ib, 1);
        idx_2 = idx{Iidx}(Ib, 2);
    
        bytes_values(Ib, idea_counter) = (A(idx_1, 1)-A(idx_1, 2)) + (A(idx_2, 1)-A(idx_2, 2));
    end
    idea_counter = idea_counter + 1;
end
    
    % Modulo option
keys = [reshape(dec2hex(mod(bytes_values(:, 1), 256))',1,[])];
for Ic = 2:size(bytes_values,2)  
     keys = [keys; reshape(dec2hex(mod(bytes_values(:, Ic), 256))',1,[])];
end

    % Dummy normalization with floor
for Ic = 1:size(bytes_values,2)  
     keys = [keys; reshape(dec2hex( floor((bytes_values(:, Ic) / max(bytes_values(:, Ic)))*255) )',1,[])];
end

    % Better normalization with floor
for Ic = 1:size(bytes_values,2)  
     keys = [keys; reshape(dec2hex( floor( ( (bytes_values(:, Ic)-min(bytes_values(:, Ic))) / (max(bytes_values(:, Ic))-min(bytes_values(:, Ic))) )*255) )',1,[])];
end


%% Write composed keys into file_in_loadpath
fid = fopen('keys.txt', 'w+');
for i=1:size(keys, 1)
    fprintf(fid, '%s', keys(i,:));
    fprintf(fid, '\n');
end
fclose(fid);