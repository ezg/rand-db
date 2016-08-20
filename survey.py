#!/usr/bin/env python
import csv
import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

from scipy.stats.stats import pearsonr

survey_path = './survey.csv'

checkbox_attrs = ['Answer.FavoriteFood', 'Answer.Pet', 'Answer.Fruit', 'Answer.Politician', 'Answer.MusicGenre', 'Answer.SocialMedia', 'Answer.ColorSocks', 'Answer.FootballTeam', 'Answer.MusicInstrument', 'Answer.Sport', 'Answer.Event']

number_attrs = ['Answer.HolidayDestination', 'Answer.Age', 'Answer.Height', 'Answer.Siblings', 'Answer.Pillow', 'Answer.ChildrenWant', 'Answer.CreditCard', 'Answer.Car', 'Answer.ChildrenHave', 'Answer.CountriesBeenTo', 'Answer.BookRead', 'Answer.BookOwned', 'Answer.Coffee', 'Answer.InternetUsage', 'Answer.TV', 'Answer.ApplePerMonth', 'Answer.ExerciseWeekly']

id_attrs = ['assignment-id']

radio_attrs = ['Answer.Alien', 'Answer.CityOrSuburb', 'Answer.marijuana', 'Answer.HairDrying', 'Answer.MailService', 'Answer.Brexit', 'Answer.SQL', 'Answer.Education', 'Answer.NuclearEnergy', 'Answer.GameOfThrones', 'Answer.Snow', 'Answer.LikeCountry', 'Answer.Unicorn', 'Answer.CarTransmission', 'Answer.InternetBrowser', 'Answer.Database', 'Answer.Tennis', 'Answer.Smoke', 'Answer.Bluegrass', 'Answer.EyeColor', 'Answer.PokemonGo', 'Answer.Sudoku', 'Answer.WritingHand', 'Answer.GMO', 'Answer.Skydiving', 'Answer.BathOrShower', 'Answer.Vacation', 'Answer.StartupOrCorporation', 'Answer.Olympics', 'Answer.GunControl', 'Answer.Religious', 'Answer.Potato', 'Answer.Continent', 'Answer.Juggle', 'Answer.PhoneBrand', 'Answer.MaritalStatus', 'Answer.GlobalEconomy', 'Answer.Sauna', 'Answer.OnlineShopping', 'Answer.Lesson', 'Answer.Kindle', 'Answer.SmartphoneOS', 'Answer.FlightSeat', 'Answer.DinerWith', 'Answer.HouseHoldIncome', 'Answer.Stonebraker', 'Answer.Drunk', 'Answer.JumpOnOneFoot', 'Answer.Rain', 'Answer.JobMoneyOrFun', 'Answer.Gender', 'Answer.GlobalWarming', 'Answer.ScaryMovie', 'Answer.CuteAnimal', 'Answer.Darwin', 'Answer.ElectricOrGasCar', 'Answer.LeiaOrSkywalker', 'Answer.RentOrBuyHouse', 'Answer.Cook', 'Answer.earlobe', 'Answer.DNA', 'Answer.DrinkForDinner', 'Answer.Gym', 'Answer.SunriseOrSunset', 'Answer.Paris', 'Answer.Astrology', 'Answer.Film', 'Answer.HairColor', 'Answer.Newspaper']

def main():
    seedb_one('Answer.Alien', '1', 'Answer.StartupOrCorporation', 'Answer.Potato', '2')
    seedb_one('Answer.Alien', '2' , 'Answer.StartupOrCorporation', 'Answer.Potato', '2')
    seedb_one('Answer.CityOrSuburb', '1', 'Answer.StartupOrCorporation','Answer.Potato', '2')
    seedb_one('Answer.HairDrying', '2' , 'Answer.StartupOrCorporation', 'Answer.Potato', '2')






def seedb_one(filter_attr, filter_val, group_attr, aggr_attr, aggr_val):
    survey = load_survey_table()

    #filter_attr = 'Answer.Alien'
    #group_attr = 'Answer.StartupOrCorporation'
    #aggr_attr = 'Answer.Sudoku'
    #aggr_val = '2'
    refer_view = (
            survey.project(
                [group_attr, aggr_attr])
            .group_aggregate(
                [group_attr], [aggr_attr],
                #lambda t_group: t_group.filter(
                #    lambda t_row: t_row.at(aggr_attr) == aggr_val
                #    ).num_rows,
                lambda t_group: len(list(filter(lambda x: x == aggr_val, t_group.col_at(aggr_attr)))),
                'aggr')
            )
    assert refer_view.num_rows > 0

    #filter_val = '2'
    target_view = (
            survey.filter(lambda t_row: t_row.at(filter_attr) == filter_val)
            .project(
                [group_attr, aggr_attr])
            .group_aggregate(
                [group_attr], [aggr_attr],
                #lambda t_group: t_group.filter(
                #    lambda t_row: t_row.at(aggr_attr) == aggr_val
                #    ).num_rows,
                lambda t_group: len(list(filter(lambda x: x == aggr_val, t_group.col_at(aggr_attr)))),
                'aggr')
            )
    refer_p = normalize(refer_view.col_at('aggr'))
    target_p = normalize(target_view.col_at('aggr'))
    assert sum(target_p) > 0
    dist = distance(refer_p, target_p)
    assert dist > seedb_fig1a_distance()
    print(filter_attr, ',', filter_val, ',', group_attr, ',', aggr_attr, ',', aggr_val, ',', dist)
    print('refer_view', refer_view)
    print('target_view', target_view)

    ## Plot
    #target_stats = dict(zip(target_view.col_at(group_attr), normalize(target_view.col_at('aggr'))))
    #refer_stats = dict(zip(refer_view.col_at(group_attr), normalize(refer_view.col_at('aggr'))))

    #opacity = 0.4
    #bar_width = 0.35
    #n_bars = 2
    #index = np.arange(n_bars)
    #target_bars = plt.bar(index, [target_stats[k] for k in sorted(target_stats)], bar_width, alpha=opacity, color='b')
    #refer_bars = plt.bar(index + bar_width, [refer_stats[k] for k in sorted(refer_stats)], bar_width, alpha=opacity, color='y')
    #plt.xticks(index + bar_width, ['Startup', 'Corporation'])
    #plt.xlabel('Workplace preference')
    #plt.ylabel('# people with Sudoku incapability (normalized)')
    #target_bars.set_label('Target: Disbelief in alien existence')
    #refer_bars.set_label('Reference: All')
    ##plt.legend((target_bars[0], refer_bars[0]), ('Target: Disbelief in alien existence', 'Reference: All'))
    #plt.legend(loc='upper left')

    #plt.tight_layout()
    #plt.show()


def seedb_vary_filter_attr():
    print('seedb-vary-filter-attr')
    print('attributes of multple choices,', len(radio_attrs))
    survey = load_survey_table()

    n_target_refer_pairs = 0
    for group_attr in radio_attrs:
        for aggr_attr in set(radio_attrs) - set([group_attr]):
            aggr_vals = list(set(survey.col_at(aggr_attr)))
            for aggr_val in aggr_vals[:-1]:
                refer_view = (
                        survey.project(
                            [group_attr, aggr_attr])
                        .group_aggregate(
                            [group_attr], [aggr_attr],
                            #lambda t_group: t_group.filter(
                            #    lambda t_row: t_row.at(aggr_attr) == aggr_val
                            #    ).num_rows,
                            lambda t_group: len(list(filter(lambda x: x == aggr_val, t_group.col_at(aggr_attr)))),
                            'aggr')
                        )
                assert refer_view.num_rows > 0

                for filter_attr in set(radio_attrs) - set([group_attr, aggr_attr]):
                    filter_vals = set(survey.col_at(filter_attr))
                    for filter_val in filter_vals:
                        target_view = (
                                survey.filter(lambda t_row: t_row.at(filter_attr) == filter_val)
                                .project(
                                    [group_attr, aggr_attr])
                                .group_aggregate(
                                    [group_attr], [aggr_attr],
                                    #lambda t_group: t_group.filter(
                                    #    lambda t_row: t_row.at(aggr_attr) == aggr_val
                                    #    ).num_rows,
                                    lambda t_group: len(list(filter(lambda x: x == aggr_val, t_group.col_at(aggr_attr)))),
                                    'aggr')
                                )
                        refer_p = normalize(refer_view.col_at('aggr'))
                        target_p = normalize(target_view.col_at('aggr'))
                        if sum(target_p) > 0:
                            dist = distance(refer_p, target_p)
                            if dist > seedb_fig1a_distance():
                                print(filter_attr, ',', filter_val, ',', group_attr, ',', aggr_attr, ',', aggr_val, ',', dist)
                        n_target_refer_pairs += 1

    print('n_target_refer_pairs,', n_target_refer_pairs)



def seedb_vary_filter_value():
    print('attributes of multple choices,', len(radio_attrs))
    survey = load_survey_table()

    n_target_refer_pairs = 0
    for filter_attr in radio_attrs:
        for group_attr in set(radio_attrs) - set([filter_attr]):
            for aggr_attr in set(radio_attrs) - set([filter_attr, group_attr]):

                aggr_vals = list(set(survey.col_at(aggr_attr)))
                for aggr_val in aggr_vals[:-1]:
                    refer_view = (
                            survey.project(
                                [group_attr, aggr_attr])
                            .group_aggregate(
                                [group_attr], [aggr_attr],
                                #lambda t_group: t_group.filter(
                                #    lambda t_row: t_row.at(aggr_attr) == aggr_val
                                #    ).num_rows,
                                lambda t_group: len(list(filter(lambda x: x == aggr_val, t_group.col_at(aggr_attr)))),
                                'aggr')
                            )
                    assert refer_view.num_rows > 0

                    filter_vals = set(survey.col_at(filter_attr))
                    for filter_val in filter_vals:
                        target_view = (
                                survey.filter(lambda t_row: t_row.at(filter_attr) == filter_val)
                                .project(
                                    [group_attr, aggr_attr])
                                .group_aggregate(
                                    [group_attr], [aggr_attr],
                                    #lambda t_group: t_group.filter(
                                    #    lambda t_row: t_row.at(aggr_attr) == aggr_val
                                    #    ).num_rows,
                                    lambda t_group: len(list(filter(lambda x: x == aggr_val, t_group.col_at(aggr_attr)))),
                                    'aggr')
                                )
                        refer_p = normalize(refer_view.col_at('aggr'))
                        target_p = normalize(target_view.col_at('aggr'))
                        if sum(target_p) > 0:
                            dist = distance(refer_p, target_p)
                            if dist > seedb_fig1a_distance():
                                print(filter_attr, ',', filter_val, ',', group_attr, ',', aggr_attr, ',', aggr_val, ',', dist)
                        n_target_refer_pairs += 1

    print('n_target_refer_pairs,', n_target_refer_pairs)


def distance(xs, ys):
    diff_vec = map(lambda x, y: x - y, xs, ys)
    return math.sqrt(sum(map(lambda x: x * x, diff_vec)))

def normalize(xs):
    sum_xs = sum(xs)
    if sum_xs == 0:
        return xs
    return [x / sum_xs for x in xs]

def seedb_fig1a_distance():
    return distance(normalize([380, 356]), normalize([758, 1657]))


def correlation():
    survey = load_survey_table()
    #print(survey)
    #attr_set = set(survey.attrs)
    #assert set(checkbox_attrs) < attr_set
    #assert set(text_attrs) < attr_set
    #assert set(number_attrs) < attr_set
    #print(attr_set - set(checkbox_attrs) - set(text_attrs) - set(number_attrs))
    #print(survey.col_at(id_attrs[0]))

    #ages = list(map(int, survey.col_at('Answer.Age')))
    #city_or_suburbs = list(map(int, survey.col_at('Answer.CityOrSuburb')))
    #ans = pearsonr(ages, city_or_suburbs)
    #print(ans)

    pearsons = dict()
    test_attrs = set(radio_attrs + number_attrs)
    for x_attr in test_attrs:
        x_col = list(map(int, survey.col_at(x_attr)))
        for y_attr in (test_attrs - set([x_attr])):
            if (x_attr, y_attr) not in pearsons and (y_attr, x_attr) not in pearsons:
                y_col = list(map(int, survey.col_at(y_attr)))
                # pearsonr(x, y) -> (correl-coef, p-value)
                pearsons[(x_attr, y_attr)] = pearsonr(x_col, y_col)

    sorted_pearsons = sorted(list(pearsons.items()), key=lambda p: p[1][1], reverse=False)
    #print(sorted_pearsons)
    for p in sorted_pearsons:
        print(p[0][0], ',', p[0][1], ',', p[1][0], ',', p[1][1])


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


def load_survey_table():
    with open(survey_path, newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')

        rows = [row for row in reader]
        assert len(rows) > 1
        # first row is column ids
        # second row is column names
        attrs = rows[1]
        mtrx = rows[2:]
        return Table(attrs, mtrx)


class Table:
    # Row-major matrix
    def __init__(self, attrs, mtrx):
        assert len(mtrx) > 0
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

    def col_at(self, attr):
        assert attr in self.attrs
        col = self.attrs.index(attr)
        return [row[col] for row in self.mtrx]

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


def test_table():
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

    print(table.group_aggregate(['d', 'b'], ['a', 'c'], lambda t: t.num_rows, 'count'))



if __name__ == '__main__':
    main()
