clear; clf;
p = 0.5;
figure('Name', 'pdf');
hold on;
N = [10, 20, 40];
% legend
legs = cell(size(N));
for i = 1:size(N, 2)
    legs{1,i} = strcat('n=', num2str(N(i)));   
end

for n = N
    pmf = [];
    for i = 0:n
        pmf = [pmf, nchoosek(n, i) * p^i * (1 - p)^(n - i)];
    end
    scatter(0:n, pmf);
end
hold off;
legend(legs);

% cdf
% figure('Name', 'cdf');
% hold on;
% n_cdfs = cumsum(n_pmfs, 2);
% for i = 1:size(N,2)
%     scatter(0:N(i), n_cdfs(i, :));
% end
% hold off;
% legend(legs);