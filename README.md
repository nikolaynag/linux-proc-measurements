# Pure python scripts for performance measurements based on linux /proc and /sys filesystems

This is a set of tools written as pure python scripts without any external dependencies. Just copy script to target server and run it with python interpreter (both 2.x and 3.x is OK). Check source code to understand what exactly is measured.

## Get user and system CPU time consumed by target process

Use `linux-cpu-usage` script to get CPU time counters from `/proc/[pid]/stat`. By default it just prints current `utime`, `stime`, `cutime` and `cstime` (see `man 5 proc`) as comma-separated float values in seconds.

You can store script output before some work is done by process and run script afterwards passing stored value as `--delta-from` argument to get counters change between two measurements.

Use `--total` argument to get total CPU usage in seconds or `--efficiency-for-amount` to get CPU efficiency for given amount of work (i.e. given amount divided by total CPU usage time in seconds).

Target process could be identified ether directly by it's `PID`, or using regular expression for command line.

See also `./linux-cpu-usage --help`.

Usage examples:

    $ ./linux-cpu-usage -c sshd
    0.16,0.18,0.00,0.00

    $ start=$(./linux-cpu-usage -c Xorg); \
        sleep 10s; \
        ./linux-cpu-usage -c Xorg -d $start
    0.13,0.09,0.00,0.00

    $ ./linux-cpu-usage -p 2740 -t
    15742.11

## Measure network counters change rate

The `linux-net-rate` is a simple tool measuring rate of change for network interface counters in `/sys/class/net/{interface}/statistics`.

Usage example:

    ./linux-net-rate -i 0.1 -c 5 bond0:tx_bytes:8 bond0:rx_bytes:8 bond0:tx_errors
    time         bond0:tx_bytes:8     bond0:rx_bytes:8      bond0:tx_errors
    22:03:53               8.694G             665.331M               0.000
    22:03:53               8.356G             707.296M               0.000
    22:03:53               7.760G               1.240G               0.000
    22:03:53               7.822G             406.817M               0.000
    22:03:53               8.272G             224.498M               0.000
