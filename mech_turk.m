clear all; close all;
n_questions = 100;
t_question = 10; % seconds

% 10c/min
% https://www.reddit.com/r/mturk/comments/1z4sma/new_to_mturk_heres_what_you_should_know/
d_min = 0.10; % dollars
n_secs_per_min = 60;

d_assignment = t_question * n_questions / n_secs_per_min * d_min;

n_workers = 100;

d_total = n_workers * d_assignment;