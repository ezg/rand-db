#!/usr/bin/env python
import csv
from scipy.stats.stats import pearsonr

survey_path = './survey.csv'

checkbox_attrs = ['Answer.FavoriteFood', 'Answer.Pet', 'Answer.Fruit', 'Answer.Politician', 'Answer.MusicGenre', 'Answer.SocialMedia', 'Answer.ColorSocks', 'Answer.FootballTeam', 'Answer.MusicInstrument', 'Answer.Sport', 'Answer.Event']

number_attrs = ['Answer.HolidayDestination', 'Answer.Age', 'Answer.Height', 'Answer.Siblings', 'Answer.Pillow', 'Answer.ChildrenWant', 'Answer.CreditCard', 'Answer.Car', 'Answer.ChildrenHave', 'Answer.CountriesBeenTo', 'Answer.BookRead', 'Answer.BookOwned', 'Answer.Coffee', 'Answer.InternetUsage', 'Answer.TV', 'Answer.ApplePerMonth', 'Answer.ExerciseWeekly']

id_attrs = ['assignment-id']

radio_attrs = ['Answer.Alien', 'Answer.CityOrSuburb', 'Answer.marijuana', 'Answer.HairDrying', 'Answer.MailService', 'Answer.Brexit', 'Answer.SQL', 'Answer.Education', 'Answer.NuclearEnergy', 'Answer.GameOfThrones', 'Answer.Snow', 'Answer.LikeCountry', 'Answer.Unicorn', 'Answer.CarTransmission', 'Answer.InternetBrowser', 'Answer.Database', 'Answer.Tennis', 'Answer.Smoke', 'Answer.Bluegrass', 'Answer.EyeColor', 'Answer.PokemonGo', 'Answer.Sudoku', 'Answer.WritingHand', 'Answer.GMO', 'Answer.Skydiving', 'Answer.BathOrShower', 'Answer.Vacation', 'Answer.StartupOrCorporation', 'Answer.Olympics', 'Answer.GunControl', 'Answer.Religious', 'Answer.Potato', 'Answer.Continent', 'Answer.Juggle', 'Answer.PhoneBrand', 'Answer.MaritalStatus', 'Answer.GlobalEconomy', 'Answer.Sauna', 'Answer.OnlineShopping', 'Answer.Lesson', 'Answer.Kindle', 'Answer.SmartphoneOS', 'Answer.FlightSeat', 'Answer.DinerWith', 'Answer.HouseHoldIncome', 'Answer.Stonebraker', 'Answer.Drunk', 'Answer.JumpOnOneFoot', 'Answer.Rain', 'Answer.JobMoneyOrFun', 'Answer.Gender', 'Answer.GlobalWarming', 'Answer.ScaryMovie', 'Answer.CuteAnimal', 'Answer.Darwin', 'Answer.ElectricOrGasCar', 'Answer.LeiaOrSkywalker', 'Answer.RentOrBuyHouse', 'Answer.Cook', 'Answer.earlobe', 'Answer.DNA', 'Answer.DrinkForDinner', 'Answer.Gym', 'Answer.SunriseOrSunset', 'Answer.Paris', 'Answer.Astrology', 'Answer.Film', 'Answer.HairColor', 'Answer.Newspaper']

def main():
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
