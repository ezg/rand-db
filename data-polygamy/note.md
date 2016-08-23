# Data-polygamy commit
7d5fb5c

# CIDR paper
- The experiments are stored in exp1a-100r and exp10a-100r.  'a' means attributes, and 'r' means records.
- The suplemental experiments are stored just in expXa-Yr.result, and were run with the master script `rand.sh`.  

# Rounding of confidencen level
For exp10a-100r, we rounded the confience level to two decimal places, so the trial with 0.047 p-value was rounded up to 0.05, and we counted it as a true rejection.

# Docker
The exp was conducted on docker zheguang/study, on bsn03.

# Data
Data is stored in directory `dp/`.  The `datasets.txt` file is a schema file for for Data-Polygamy.
