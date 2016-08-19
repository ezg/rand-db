% Output from survey.py
% Answer.Alien , 2 , Answer.StartupOrCorporation , Answer.Sudoku , 2 , 0.4400874372419771
% refer_view Answer.StartupOrCorporation, aggr
% ['1', 21]
% ['2', 18]
% 
% target_view Answer.StartupOrCorporation, aggr
% ['1', 5]
% ['2', 17]

refer_stats = normalize([21; 18]);
target_stats = normalize([5; 17]);
n_bars = size(refer_stats, 1);

y_groups = [target_stats, refer_stats];

hold on;
xticks = 1:n_bars;
bar(xticks, y_groups);
ax = gca; % necessary
ax.XTick = xticks;
ax.XTickLabel = {'Startup', 'Corporation'};
ax.FontSize = 18;
xlabel('Workplace preference');
ylabel('% Sudoku-unable');
legend({'Target filter: Disbelief in alien existence'; 'Reference filter: Any'}, 'location', 'SouthOutside'); 
hold off;