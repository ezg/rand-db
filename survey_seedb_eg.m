clear; close all;
% Output from survey.py
% Answer.Alien , 2 , Answer.StartupOrCorporation , Answer.Sudoku , 2 , 0.4400874372419771
% refer_view Answer.StartupOrCorporation, aggr
% ['1', 21]
% ['2', 18]
% 
% target_view Answer.StartupOrCorporation, aggr
% ['1', 5]
% ['2', 17]

% refer_stats = normalize([21; 18]);
% target_stats = normalize([5; 17]);
% n_bars = size(refer_stats, 1);
% 
% y_groups = [target_stats, refer_stats];
% 
% hold on;
% xticks = 1:n_bars;
% bar(xticks, y_groups);
% ax = gca; % necessary
% ax.XTick = xticks;
% ax.XTickLabel = {'Startup', 'Corporation'};
% ax.FontSize = 18;
% xlabel('Workplace preference');
% ylabel('% Sudoku-unable');
% legend({'Target filter: Disbelief in alien existence'; 'Reference filter: Any'}, 'location', 'SouthOutside'); 
% hold off;

% Answer.Alien , 1 , Answer.StartupOrCorporation , Answer.Potato , 2 , 0.40406101782088427
% refer_view Answer.StartupOrCorporation, aggr
% ['2', 6]
% ['1', 15]
% 
% target_view Answer.StartupOrCorporation, aggr
% ['2', 0]
% ['1', 12]
% 
% Answer.Alien , 2 , Answer.StartupOrCorporation , Answer.Potato , 2 , 0.538748023761179
% target_view Answer.StartupOrCorporation, aggr
% ['2', 6]
% ['1', 3]
% 
% Answer.HairDrying , 2 , Answer.StartupOrCorporation , Answer.Potato , 2 , 0.30304576336566325
% target_view Answer.StartupOrCorporation, aggr
% ['2', 2]
% ['1', 2]

refer = normalize([15, 6]);
target_alien1 = normalize([12, 0]);
target_alien2 = normalize([3, 6]);
target_hairdry2 = normalize([2, 2]);

n_bars = size(refer, 2);

ys = [refer; target_alien1; target_alien2; target_hairdry2];
xls = {'Filter: All', 'Filter: Belief in Alien Existence', 'Filter: Disbelief in Alien Existence', 'Filter: Prefer Blow Hair Drying'};

for i = 1:size(ys, 1)
    fh = figure;
    fh.Position = [0, 0, 520, 280];
    hold on;
    xticks = 1:n_bars;
    bar_width = 0.7;
    bar(xticks, ys(i, :), bar_width);
    ax = gca; % necessary
    ax.XTick = xticks;
    ax.XTickLabel = {'Startup', 'Corporation'};
    ax.FontSize = 20;
    xlabel(xls(i));
    ylabel('% Cheddar & Sour Cream');
    title('Potato Chips vs Workspace Preference');
    hold off;
end
