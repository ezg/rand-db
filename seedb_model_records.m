clear; clf;
close all;

p_seedb = []; % columns for different N, rows for different trials
n_repeat = 100;
Ns = [100, 100*10, 100*100, 100*1000];
for N = Ns
    N_white = N / 2;
    N_black = N - N_white;
    assert(N_white == N_black);
    p_col2_1 = 0.5; % P(col1 = 1) = 0.5
    
    k = 6; % card of filter col    
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
bar(1:size(Ns,2), avg_p_seedb);
errorbar(1:size(Ns,2), avg_p_seedb, std_p_seedb, 'r.');
hold off;
set(gca, 'XTick', [1, 2, 3, 4]);
set(gca, 'XTickLabel', ['1e2'; '1e3'; '1e4'; '1e5']);
xlabel('# records');
ylabel('probability');
title('Interestingness >= SeeDB Fig 1(a), filter column cardinality=6');
desc = 'Reference view on base table; Filter column cardinality=6.';
legend(desc, 'location', 'SouthOutside'); 
