from ping3 import ping, verbose_ping
from matplotlib import pyplot as plt
from time import sleep, time, ctime
from itertools import cycle
from ipaddress import ip_address
import sys

graph_delay = .05
cycol = cycle('bgrcmk')

if __name__ == '__main__':
    test_ips = []

    argc = len(sys.argv) - 1
    if not argc:
        test_ips.append('192.168.0.1')
        test_ips.append('8.8.8.8')
    else:
        for arg in sys.argv[1:]:
            test_arg = arg.strip().replace('"', '').replace("'", "")
            test_arg = ip_address(test_arg)
            test_ips.append(test_arg)

    if not test_ips:
        raise RuntimeError("No valid IP address passed")

    # Default values in times allow for average to be taken to plot dropped packets nicely
    results = {}
    for ip in test_ips:
        results[ip] = {'return time': [.1], 'graph_color': next(cycol), 'times': [int(time())], 'lost': []}

    start = int(time())

    fig = plt.figure()
    fig.canvas.manager.set_window_title("Internet Drop Tracker")
    plt.ion()
    plt.show()
    while True:
        plt.clf()

        plt.title("Ping return times (in seconds)")
        plt.ylabel("Return Time (s)")
        plt.xlabel("Time of Event")
        for ip in results.keys():

            result = ping(format(ip))
            if not result:
                results[ip]['lost'].append(int(time()))
            else:
                last_x_increment = 10

                results[ip]['times'].append(int(time()))
                results[ip]['return time'].append(result)

            x_legend = list(map(ctime, results[ip]['times'][1:]))
            plt.plot(x_legend, results[ip]['return time'][1:], color=results[ip]['graph_color'], alpha=.5,
                     label=f"Pinging {ip}")

            if results[ip]['lost']:
                x_legend = list(map(ctime, results[ip]['lost']))
                y_legend = [(max(results[ip]['return time'][1:]) + min(results[ip]['return time'][1:])) / 2] * \
                           len(results[ip]['lost'])
                plt.scatter(x_legend, y_legend, marker='o', label=f"Drops to {ip}", c=results[ip]['graph_color'])
                for x,y in zip(x_legend, y_legend):
                    plt.text(x, y, 'Drop', horizontalalignment='right')

        #plt.grid(xdata=results[ip]['times'][1:], ydata=results[ip]['return time'][1:])
        plt.minorticks_on()
        plt.grid(which='minor')
        plt.grid(which='major')
        times = results[list(results.keys())[0]]['times'][1:]
        x_times = [times[0], times[int(len(times) * .25)], times[int(len(times) * .5)], times[int(len(times) * .75)],
                   times[-1]]
        x_times = list(map(ctime, x_times))
        plt.xticks(x_times, rotation=15)
        plt.legend(loc='upper left')
        plt.draw()
        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.start_event_loop(0.05)

        sleep(graph_delay)
