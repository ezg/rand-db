#!/usr/bin/env python

import numpy

# interval = num secs in two weeks
t_interval = 60 * 60 * 12 * 7 * 2
t_start = 900000000
x_default = 0.5
n_xs = 100 # excluding time
p_outlier = 0.2
n_attrs = 1

def main():
    for i in range(0, n_xs):
        def gen_x():
            is_outlier = numpy.random.uniform()
            if is_outlier <= p_outlier:
                x = numpy.random.uniform()
            else:
                x = x_default
            return x

        x = ','.join(['{0:.2f}'.format(gen_x()) for _ in range(0,  n_attrs)])

        print('{},{}'.format(t_start + i * t_interval, x))


if __name__ == '__main__':
    main()

