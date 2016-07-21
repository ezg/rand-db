#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>
#include <sstream>
#include <random>
#include <map>

using namespace std;

unsigned seed = 11;
default_random_engine generator(seed);

typedef int32_t Datum;
typedef uint32_t col_id_t;

template<typename T>
string vec_str(const vector<T>& p) {
    ostringstream oss;
    oss << "[";
    for (auto x : p) {
        oss << x << ",";
    }
    oss << "]";
    return oss.str();
}

struct Column {
    vector<Datum> _data;

    string as_str() {
        return vec_str(_data);
    }
};

enum Compare {
    EQ = 0,
};

struct Predicate {
    col_id_t _col;
    Compare _compare;
    Datum _arg;

    string as_str() const {
        ostringstream oss;
        assert(_compare == EQ);
        oss << "{Predicate: col0 == " << _arg << "}";
        return oss.str();
    }
};

struct AvgState {
    double _sum;
    size_t _count;

    string as_str() const {
        ostringstream oss;
        oss << "{AvgState: {sum: " << _sum << ", count: " << _count << "}";
        return oss.str();
    }

    double avg() const {
        return _sum / _count;
    };
};

struct Table {
    vector<Column> _cols;

    map<vector<Datum>,AvgState> select_group_by_aggregate(const vector<Predicate>& filter_by, const vector<col_id_t>& group_by, col_id_t aggregate_by) const {
        //map<vector<Datum>,double> group_avgs;
        map<vector<Datum>,AvgState> group_states;

        size_t n_tuples = _cols.at(0)._data.size();

        vector<size_t> selected_tids;
        for (size_t i = 0; i < n_tuples; i++) {
            bool selected = true;
            for (auto& pred : filter_by) {
                assert(pred._compare == EQ);
                if (_cols.at(pred._col)._data.at(i) != pred._arg) {
                    selected = false;
                    break;
                }
            }
            if (selected) {
                selected_tids.push_back(i);
            }
        }

        for (auto& i : selected_tids) {
            vector<Datum> group_data;
            for (auto& g : group_by) {
                group_data.push_back(_cols.at(g)._data.at(i));
            }
            if (group_states.find(group_data) == group_states.end()) {
                group_states.insert({group_data, {0.0, 0}});
            }
            group_states.at(group_data)._sum += _cols.at(aggregate_by)._data.at(i);
            group_states.at(group_data)._count += 1;
        }

        return group_states;

    }
};

double euclidean_dist(const vector<double>& p1, const vector<double>& p2) {
    assert(p1.size() == p2.size());
    double sum_squared_dist = 0.0;
    for (int i = 0; i < p1.size(); i++) {
        sum_squared_dist += (p1[0] - p2[0]) * (p1[0] - p2[0]);
    }
    return sqrt(sum_squared_dist);
}

vector<double> normalize(const vector<double>& p) {
    double sum = 0.0;
    for (auto x : p) {
        sum += x;
    }
    vector<double> res;
    for (auto x : p) {
        res.push_back(x / sum);
    }
    return res;
}

struct UniformRandRange {
    Datum _lo;
    Datum _hi;
    uniform_int_distribution<int> _pdf;

    UniformRandRange(Datum lo, Datum hi):
            _lo(lo), _hi(hi), _pdf((int)lo, (int)hi)
    {
        assert(lo < hi && INT_MIN <= lo && lo <= INT_MAX && INT_MIN <= hi && hi <= INT_MAX);
    }

    Datum next() {
        int res = _pdf(generator);
        return Datum(res);
    }
};

struct Range {
    Datum _lo;
    Datum _hi;

    string as_str() const {
        ostringstream oss;
        oss << "[" << _lo << "," << _hi << "]";
        return oss.str();
    }
};

Column uniform_rand_col(size_t n_tuples, const Range& closed_interval) {
    UniformRandRange rand_range(int(closed_interval._lo), int(closed_interval._hi));
    Column col;
    for (size_t i = 0; i < n_tuples; i++) {
        col._data.push_back(rand_range.next());
    }
    return col;
}

void uniform_rand_range_test() {
    size_t n_tuples = 1e+5;
    Column col = uniform_rand_col(n_tuples, Range {0, 1});

    size_t n_one = 0;
    for (auto x : col._data) {
        if (x == 1) {
            n_one++;
        }
    }

    cout << double(n_one) / double(n_tuples) << endl;
}

struct BarChart {
    map<vector<Datum>,double> _bars;

    void extend_from(const BarChart& other) {
        for (auto& b : other._bars) {
            if (_bars.find(b.first) == _bars.end()) {
                _bars[b.first] = 0.0;
            }
        }
    };

    vector<double> as_points() const {
        vector<double> p;
        for (auto& b : _bars) {
            p.push_back(b.second);
        }
        return p;
    }

    double deviate_from(const BarChart& other) const {
        assert(_bars.size() == other._bars.size());
        for (auto& b : other._bars) {
            assert(_bars.find(b.first) != _bars.end());
        }

        return euclidean_dist(normalize(as_points()), normalize(other.as_points()));
    }

    string as_str() const {
        ostringstream oss;
        oss << "{BarChart: {bars: [";
        for (auto& b : _bars) {
            oss << "{x:" << vec_str(b.first) << ",y:" << b.second << "},";
        }
        oss << "]}}";
        return oss.str();
    }
};

BarChart bars_3col_table(const Table& t, const Predicate& col0_pred) {
    // select avg(col2)
    // from table
    // where col0 = val
    // group by col1
    vector<col_id_t> group_by = {1};
    col_id_t aggregate_by = 2;

    map<vector<Datum>, AvgState> group_states = t.select_group_by_aggregate({ col0_pred }, group_by, aggregate_by);

    //map<vector<Datum>,double> bars;
    BarChart chart;
    //cout << "bars_3col_table col0_pred: " << col0_pred.as_str() << endl;
    for (auto& ga: group_states) {
        //cout << "group: " << vec_str(ga.first) << ", state: " << ga.second.as_str() << ", avg: " << ga.second.avg() << endl;
        assert(chart._bars.find(ga.first) == chart._bars.end());
        chart._bars[ga.first] = ga.second.avg();
    }
    return chart;
}

/**
 * Exp
 */
void exp_col_range(size_t n_tuples, const vector<Range>& col_ranges) {

    cout << "exp_col_range: n_tuples=" << n_tuples << ", col_ranges=";
    for (auto& r : col_ranges) {
        cout << r.as_str() << ",";
    }
    cout << endl;

    Table t;
    //size_t n_tuples = 100;
    for (auto& r : col_ranges) {
        t._cols.push_back(uniform_rand_col(n_tuples, r));
    }

    BarChart bars1 = bars_3col_table(t, Predicate {0, EQ, 1});
    BarChart bars2 = bars_3col_table(t, Predicate {0, EQ, 2});

    //cout << "bars1: " << bars1.as_str() << endl;
    //cout << "bars2: " << bars2.as_str() << endl;

    // bars1 and bars2 may have different group values.
    // Need to add 0-agg-value bars to bars1 and bars2.
    bars1.extend_from(bars2);
    bars2.extend_from(bars1);

    //cout << "extended" << endl;
    //cout << "bars1: " << bars1.as_str() << endl;
    //cout << "bars2: " << bars2.as_str() << endl;

    cout << "dist: " << bars1.deviate_from(bars2) << endl;

}


int main() {
    const size_t n_tuples = 1000;
    cout << "n_tuples: " << n_tuples << endl;
    int multiplier = 10;
    for (Datum i = 1; i <= n_tuples; i *= multiplier) {
        for (Datum j = 1; j <= n_tuples; j *= multiplier) {
            for (Datum k = 1; k <= n_tuples; k *= multiplier) {
                exp_col_range(n_tuples, {{1, 1 + i}, {1, 1 + j}, {1, 1 + k}});
            }
        }
    }

    cout << "seedb: " << euclidean_dist({0.52, 0.48}, {0.31, 0.69}) << endl;

    return 0;
}

