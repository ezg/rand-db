clear; clf; close all;

% In the SeeDB Figure 2(a) scenario, we have three columns, A, B and C, and
% we have query that filters on A, groups by B, and aggregates on C.
% The question is how probable SeeDB Figure 2(a) can arise from random fair 
% coin tosses.
%
% Consider the simple case of `n` Bernoulli trials of p(1) = 0.5. We ask
% what is the relationship between `n` and the probability that the number
% of heads is deviates from the mean `0.5n` at least as much as in Figure
% 2(a).  That is, the bar chart of [#heads, #tails] deviates from [0.5n,
% 0.5n] more than Figure 2(a).
%
% The deviation is measured as treating a bar chart as a multi-dimensional 
% point. Figure 2(a) has euclidean distance 0.28 ~ 0.3.
%
% Note that this simple case effectively treats C as all 1, and the
% aggregate on C is summation.  However, it seems the variance of C would
% make a difference on the deviation as well.  This case we havnen't
% consider yet.
%
% One extension of this simple case is, instead of having just 3 columns,
% we have `m` columns, each indendent Bernoulli trials.  What is the
% relationship between `m` and the probability of deviation, while fixing
% `n`?
% 

thres = 0.2;
p_head = 0.5;
x2 = 0.5;
y2 = 0.5;

x1_right_tail = sqrt(thres^2/2) + x2;
x1_left_tail = x2 - sqrt(thres^2/2);
assert(1 - x1_right_tail == x1_left_tail);

n_prob_tails = [];
N = [10, 100, 1000];
for n = N
    k = n * x1_left_tail;

    prob_left_tail = 0.0;
    if n <= 50
        for i = 0:k
            prob_left_tail = prob_left_tail + nchoosek(n, i) * p_head^i * (1 - p_head)^(n - i);
        end
    else
        % normal approximation
        z_mean = n * p_head;
        z_std = sqrt(n * p_head * (1 - p_head));
        z = (k - z_mean) / z_std;
        prob_left_tail = normcdf(z);
    end
    n_prob_tails = [n_prob_tails, 2 * prob_left_tail];
end
figure('Name', strcat('thres=', num2str(thres)));
bar(1:size(N,2), n_prob_tails);

