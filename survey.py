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


def main():
    check_empty_cell()


if __name__ == '__main__':
    main()
