clear; clf;
close all;

num_groups = 2;

int_target_y = [380; 356];
int_ref_y = [758; 1657];

unint_target_y = [28; 28];
unint_ref_y = [44; 43];

figure;
hold on;
xticks = 1:num_groups;
M = [normalize(int_target_y) normalize(int_ref_y)];
bar(xticks, M);
ax = gca;
ax.XTick = xticks;
ax.XTickLabel = {};
ax.FontSize = 18;
xlabel('col2');
ylabel('normalized aggr(col3)');
legend({'Target' 'Reference'}, 'location', 'SouthOutside');
%title('Interesting visualization');
hold off;

figure;
hold on;
M_unint = [normalize(unint_target_y) normalize(unint_ref_y)];
bar(xticks, M_unint);
ax = gca;
ax.XTick = xticks;
ax.XTickLabel = {};
ax.FontSize = 18;
xlabel('col2');
ylabel('normalized aggr(col3)');
legend({'Target' 'Reference'}, 'location', 'SouthOutside');
%title('Uninteresting visualization');
hold off;