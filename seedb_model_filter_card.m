clear; clf;
close all;

% The SeeDB Figure 1 can be modeled as a generative process:
% (1) Shuffle equal number of black and white balls uniformly at random, 
% and lay them out as a sequence. The total number of balls is N.
% (2) Pick a ball indexed at I according to Binomial distribution of
% Bin(N,0.5).
% (3) What is the probability that the balls to the left of I have more
% black than white balls by a margin? (Or vice versa for symmetry).
%
% This process can model the chance of deviation of target query from the
% reference query (default one) as in SeeDB Figure 1.
% // Target query
% SELECT col2, avg(col3)
% FROM table
% WHERE col1 = 1
% GROUP BY col2
% // Reference query 1 (in Figure 1)
% SELECT col2, avg(col3)
% FROM table
% WHERE col1 = 0
% GROUP BY col2
% // Reference query 2 (default one)
% SELECT col2, avg(col3)
% FROM table
% GROUP BY col2
%
% Note the interpretation of the process:
% - The avg(col3) becomes count(col3) and col3 contains all 1's.
% - The filter condition on col1 can be seen as picking I, where balls to 
% the left of I is filtered.
% The reason why I is not always N/2 is because
% - I ~ Bin(N, 0.5) is for the case of col0 having two values.  For more
% values, I can be modeled as a multinomial random variable.
% - The default reference query 2 as modeled in the process is not random,
% because there are equal number of white and black balls in total.
% 
% Controlling variables:
% - col3 is not a constant 1.
% - I is multinomial random variable.

p_seedb = []; % columns for different k, rows for different trials
n_repeat = 100;

N_white = 500;
N_black = N_white;
N = N_white + N_black;
p_col2_1 = 0.5; % P(col1 = 1) = 0.5

K = 2:10;
for k = K
    p_reps = [];
    for rep = 1:n_repeat
        cards = [k, 2, 1];

        % I ~ Bin(N, p_col0_1)
        p_k = 1 / cards(1) * ones(1, cards(1));
        I = mnrnd(N, p_k);
        I = I(1);

        % more black than white balls in a margin in I
        %ref_base = 0.5 * ones(1, cards(2));
        %seedb_thres = binocdf(758, 1657, 0.5);
        p_reps = [p_reps; 2 * binocdf(floor(I * (758 / 1657)), I, p_col2_1)]; % multiplied by 2 for either #black > #white or #white > #black
        %normalize([758, 1657])
        %eucli_dist(normalize([758, 1657]), normalize([380, 356]))
    end
    p_seedb = [p_seedb, p_reps];
end
avg_p_seedb = mean(p_seedb);
std_p_seedb = std(p_seedb);
hold on;
bar(K, avg_p_seedb);
errorbar(K, avg_p_seedb, std_p_seedb, 'r.');
hold off;
xlabel('filtering column cardinality');
ylabel('probability');
title('Interestingness >= SeeDB Fig 1(a), 1000 records');
desc = 'Reference view on base table; 1000 records';
legend(desc, 'location', 'SouthOutside'); 