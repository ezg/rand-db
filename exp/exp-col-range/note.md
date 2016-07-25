# Commmit id
* 3347b15 (HEAD -> master) exp: exp_col_range ready

# output.raw

## setup
- Table: 3 columns, all int32.

- Target query:

  SELECT avg(col2)
  FROM table
  WHERE col0 = 1
  GROUP BY col1

- Reference query:
  SELECT avg(col2)
  FROM table
  WHERE col0 = 2
  GROUP BY col1

- Dataset: 1000 tupels. 

## Control parameters
- Uniform random range of each column. 

  Vary each column's random range from having interval length 1 up to `n_tuples`, with multiplier 10.  E.g. [1,2], [1,11], [1, 101], ..., [1, 1001]
