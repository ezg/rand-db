#!/usr/bin/env python
import csv

survey_path = './survey.csv'

# output:
#   assignment-id: col-num
def check_empty_cell():
    # CSV files need to be opened with empty newline.
    with open(survey_path, newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')

        for row in reader:
            f_row = filter(lambda x: not x, row)
            if list(f_row):
                print('{}: {}'.format(row[0], row.index('')))


class Table:
    # Row-major matrix
    def __init__(self, attrs, mtrx):
        assert len(attrs) == len(mtrx[0])
        self.attrs = attrs
        self.mtrx = mtrx
        self.num_rows = len(mtrx)
        self.num_cols = len(mtrx[0])

        assert not list(filter(lambda row: len(row) != self.num_cols, mtrx))

    def at(self, attr, row=0):
        assert 0 <= row and row < self.num_rows
        col = self.attrs.index(attr)
        return self.mtrx[row][col]

    def row_at(self, row):
        assert 0 <= row and row < self.num_rows
        return self.mtrx[row]

    def project(self, attrs):
        cols = [self.attrs.index(attr) for attr in attrs]
        new_mtrx = list(map(lambda row: [row[col] for col in cols], self.mtrx))
        return Table(attrs, new_mtrx)

    def filter(self, row_func):
        new_mtrx = list(filter(lambda row: row_func(Table(self.attrs, [row])), self.mtrx))
        new_attrs = self.attrs
        return Table(new_attrs, new_mtrx)

    # aggr_func: matrix -> cell
    def group_aggregate(self, group_attrs, aggr_attrs, aggr_func, aggr_name):
        assert not set(group_attrs) & set(aggr_attrs), "group-by attributes and aggregation attributes should be different"
        assert set(group_attrs) | set(aggr_attrs) == set(self.attrs), "group-by attributes plus aggregation attributes should equal to all attributes"

        group_cols = [self.attrs.index(name) for name in group_attrs]
        aggr_cols = [self.attrs.index(name) for name in aggr_attrs]

        # group rows
        gs = dict()
        for row in self.mtrx:
            g = tuple([row[col] for col in group_cols])
            aggr = [row[col] for col in aggr_cols]
            if g not in gs:
                gs[g] = []
            gs[g].append(aggr)


        # aggrgate rows
        aggr_gs = dict(map(lambda g: (g, aggr_func(Table(aggr_attrs, gs[g]))), gs))

        # form output table
        new_mtrx = list(map(lambda g: list(g) + [aggr_gs[g]], aggr_gs))
        new_attrs = group_attrs + [aggr_name]

        return Table(new_attrs, new_mtrx)

    def __str__(self):
        res = ', '.join(self.attrs) + '\n'
        for row in self.mtrx:
            res += str(row) + '\n'

        return res


def main():
    #check_empty_cell()
    mtrx = [
        [1, 2, 3, 4],
        [1 * 2, 2 * 2, 3 * 2, 4 * 2],
        [1 * 3, 2 * 3, 3 * 3, 4 * 3],
        [1 * 4, 2 * 4, 3 * 4, 4 * 4],
        [1 * 4, 2 * 4, 3 * 4, 4 * 4],
        [1 * 4, 4 * 4, 3 * 4, 2 * 4],
    ]

    attrs = ['a', 'b', 'c', 'd']

    table = Table(attrs, mtrx)
    print(table)

    print(table.at('a'))
    print(table.at('b', 2))
    print(table.at('d', 1))

    print(table.project(['d', 'b']))

    print(table.filter(lambda t: t.at('c') % 2 is 0))

    print(table.group_aggregate(['d', 'b'], ['a', 'c'], lambda table: table.num_rows, 'count'))


if __name__ == '__main__':
    main()
