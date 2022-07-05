from ping3 import ping, verbose_ping
from matplotlib import pyplot as plt
from time import sleep, time


if __name__ == '__main__':
    default_gateway = '192.168.0.1'
    destination_test = '8.8.8.8'

    results = {
        f'{default_gateway}': {'lost': 0, 'return time': [], 'graph': None},
        f'{destination_test}': {'lost': 0, 'return time': [], 'graph': None},
    }
    delay = .1

    figure, axis = plt.subplots(1, len(results.keys()))
    plt.ion()
    plt.show()

    count = 0
    for ip in results.keys():
        results[ip]['graph'] = count
        count += 1

    start = int(time())

    for x in range(10, 99999999999999):

        for ip in results.keys():

            result = ping(ip)
            if not result:
                results[ip]['lost'] += 1
            else:
                last_x_increment = 10

                results[ip]['return time'].append(result)

                axis[results[ip]['graph']].clear()
                axis[results[ip]['graph']].plot(list(range(0, len(results[ip]['return time']))),
                                                results[ip]['return time'],
                                                label=f"Pinging {ip}")
                axis[results[ip]['graph']].set_title(f"Return Time Over {int(time()) - start}s\n"
                                                     f"Packet Loss: { results[ip]['lost'] / (results[ip]['lost'] + len(results[ip]['return time'])) * 100:.2f}%\n"
                                                     f"Avg Return Time: {sum(results[ip]['return time'])/len(results[ip]['return time']):.4f}s\n"
                                                     f"Avg Over Last {last_x_increment}: {sum(results[ip]['return time'][-last_x_increment:])/last_x_increment:.4f}s\n"
                                                     f"Max Time: {max(results[ip]['return time']):.4f}s  Min Time: {min(results[ip]['return time']):.4f}s")
                axis[results[ip]['graph']].set_xlabel(f"Trials")
                axis[results[ip]['graph']].legend()
        plt.draw()
        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.start_event_loop(0.05)

        sleep(delay)

