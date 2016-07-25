#!/usr/bin/env python

from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


def avg_of(xs):
    return float(sum(xs)) / float(len(xs))


def std_of(xs):
    avg = avg_of(xs)
    return sqrt(sum(map(lambda x: pow(x - avg, 2), xs)))


def overall_false_positives():
    seedb_fig1a_dist = 0.296985
    all_n_exps = []
    all_n_false_pos = []

    for path in ['output.raw.1', 'output.raw.2', 'output.raw.3', 'output.raw.4']:
        with open(path, 'r') as file:
            n_exps = 0
            n_false_pos = 0
            for line in file:
                if line.startswith('dist:'):
                    #dist: 0.0054777
                    n_exps += 1
                    dist = float(line.strip().split(' ')[1])
                    if dist >= seedb_fig1a_dist:
                        n_false_pos += 1

            all_n_exps.append(n_exps)
            all_n_false_pos.append(n_false_pos)

    avg_n_exps = avg_of(all_n_exps)
    std_n_exps = std_of(all_n_exps)

    avg_n_false_pos = avg_of(all_n_false_pos)
    std_n_false_pos = std_of(all_n_false_pos)

    opacity = 0.4
    bar_width = 0.35
    error_config = {'ecolor': '0.3'}

    n_bars = 2
    index = np.arange(n_bars)
    barlist = plt.bar(index + bar_width / 2.0, [avg_n_exps, avg_n_false_pos], bar_width,
            alpha=opacity, yerr=[std_n_exps, std_n_false_pos], error_kw=error_config)
    barlist[0].set_color('b')
    barlist[1].set_color('r')

    plt.xticks(index + bar_width, ['# exps of varying attr ranges', '# false positives (dev. > Fig(a))'])
    plt.title('SeeDB-Fig(a)-ish query with independent uniform random attributes')

    plt.tight_layout()

    #plt.show()
    pp = PdfPages('overall_false_positives.pdf')
    plt.savefig(pp, format='pdf')
    pp.close()


def 



if __name__ == '__main__':
    main()
