#!/usr/bin/env python
import sys
import os
import time
from argparse import ArgumentParser

class RateCalculator(object):
    def __init__(self):
        self.prev_values = {}
        self.rates = {}

    def calc_rate(self, filename):
        with open(filename) as f:
            val = float(f.read().strip())
            t = time.time()
        if filename not in self.prev_values:
            self.prev_values[filename] = (t, val)
        else:
            prev_t, prev_val = self.prev_values[filename]
            self.prev_values[filename] = (t, val)
            self.rates[filename] = (val - prev_val)/(t - prev_t)

def bignum2str(num):
    for suffix in [' ','K','M','G','T','P','E','Z']:
        if abs(num) < 1000.0:
            return "{:.3f}{}".format(num, suffix)
        num /= 1000.0
    return "{:.3f}{}".format(num, "Y")

def validate_measures(args):
    measures = []
    for measure in args.measures:
        params = dict(enumerate(measure.split(":")))
        iface = params.get(0, "")
        stat = params.get(1, "")
        mul = float(params.get(2, 0))
        filename = "/sys/class/net/{}/statistics/{}".format(iface, stat)
        if not os.path.isfile(filename):
            sys.stderr.write("Wrong measure '{}': file '{}' does not exist\n".format(measure, filename))
            continue
        measures.append((measure, filename, mul))
    return measures


def main():
    parser = ArgumentParser()
    parser.add_argument("-i","--interval", type=float, help="Measure interval in seconds, default is 1 second", default=1)
    parser.add_argument("-c","--count", type=int, help="Exit after given number of measurements, no limit by default", default=0)
    parser.add_argument("measures", nargs='+', help="List of measures in 'iface_name:stat_name:mul' format, for example eth0:rx_bytes:8")
    args = parser.parse_args()

    measures = validate_measures(args)
    if len(measures) < 1:
        sys.stdout.write("\n")
        parser.print_help()
        return 0
    filenames = set((filename for _, filename, _ in measures))

    sys.stdout.write("time     {}\n".format(" ".join(["{: >20}".format(measure) for measure,_,_ in measures])))

    rc = RateCalculator()
    num = 0
    while not args.count or num <= args.count:
        columns = [time.strftime("%H:%M:%S")]
        for filename in filenames:
            rc.calc_rate(filename)
        for measure, filename, mul in measures:
            rate = rc.rates.get(filename, 0)
            if mul > 0:
                rate *= mul
            columns.append("{: >20}".format(bignum2str(rate)))
        if num > 0:
            sys.stdout.write(" ".join(columns) + "\n")
        num += 1
        time.sleep(args.interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
