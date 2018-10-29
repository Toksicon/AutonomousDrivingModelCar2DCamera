import psutil
import time

try:
    from ..server import socketio

    def processor():
        while True:
            # cpu
            socketio.emit('cpu_times', cpu_times())
            socketio.emit('cpu_percent', cpu_percent())
            socketio.emit('cpu_stats', cpu_stats())
            socketio.emit('cpu_freq', cpu_freq())

            # memory
            socketio.emit('virtual_memory', virtual_memory())
            socketio.emit('swap_memory', swap_memory())
            socketio.emit('disk_partitions', disk_partitions())
            socketio.emit('disk_usage', disk_usage())
            socketio.emit('disk_io_counters', disk_io_counters())

            # network
            socketio.emit('net_io_counters', net_io_counters())
            socketio.emit('net_connections', net_connections())
            socketio.emit('net_if_addrs', net_if_addrs())
            socketio.emit('net_if_stats', net_if_stats())

            time.sleep(1)
except:
    print('SocketIO couldn\'t be loaded')

    def processor():
        while True:
            # cpu
            print(cpu_times())
            print(cpu_percent())
            print(cpu_stats())
            print(cpu_freq())

            # memory
            print(virtual_memory())
            print(swap_memory())
            print(disk_partitions())
            print(disk_usage())
            print(disk_io_counters())

            # network
            print(net_io_counters())
            print(net_connections())
            print(net_if_addrs())
            print(net_if_stats())

            time.sleep(1)


##############################################################
# cpu

def cpu_times(percpu=True):
    def jsonify(cpu_time):
        return {
            'user': cpu_time.user,
            'system': cpu_time.system,
            'idle': cpu_time.idle,
        }

    cpu_times = psutil.cpu_times(percpu=percpu)

    if percpu:
        return [jsonify(t) for t in cpu_times]
    else:
        return jsonify(cpu_times)


def cpu_percent(percpu=True):
    return psutil.cpu_percent(interval=0, percpu=percpu)


def cpu_stats():
    stats = psutil.cpu_stats()
    return {
        'ctx_switches': stats.ctx_switches,
        'interrupts': stats.interrupts,
        'soft_interrupts': stats.soft_interrupts,   # always 0 on windows
        'syscalls': stats.syscalls                  # always 0 on linux
    }


def cpu_freq():
    freq = psutil.cpu_freq()

    return {
        'current': freq.current,
        'min': freq.min,
        'max': freq.max
    }


##############################################################
# memory

def virtual_memory():
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available
    }


def swap_memory():
    mem = psutil.swap_memory()
    return {
        'total': mem.total,
        'used': mem.used,
        'free': mem.free,
        'percent': mem.percent,
        'sin': mem.sin,
        'sout': mem.sout
    }


def disk_partitions(all=False):
    def jsonify(partition):
        return {
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'fstype': partition.fstype,
            'opts': partition.opts
        }

    partitions = psutil.disk_partitions(all=all)
    return [jsonify(d) for d in partitions]


def disk_usage(path='/'):
    disk_usage = psutil.disk_usage(path)
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free,
        'percent': disk_usage.percent
    }


def disk_io_counters(perdisk=False):
    def jsonify(counters):
        return {
            'read_count': counters.read_count,
            'write_count': counters.write_count,
            'read_bytes': counters.read_bytes,
            'write_bytes': counters.write_bytes
        }

    counters = psutil.disk_io_counters(perdisk=perdisk)

    if perdisk:
        return [jsonify(c) for c in counters.values()]
    else:
        return jsonify(counters)


##############################################################
# network


def net_io_counters(pernic=False):
    def jsonify(counters):
        return {
            'bytes_sent': counters.bytes_sent,
            'bytes_recv': counters.bytes_recv,
            'packets_sent': counters.packets_sent,
            'packets_recv': counters.packets_recv,
            'errin': counters.errin,
            'errout': counters.errout,
            'dropin': counters.dropin,
            'dropout': counters.dropout
        }

    counters = psutil.net_io_counters(pernic=pernic)

    if pernic:
        return [jsonify(c) for c in counters.values()]
    else:
        return jsonify(counters)


def net_connections(kind='inet'):
    def jsonify(connection):
        def addr(a):
            if len(a):
                return { 'ip': a.ip, 'port': a.port }

        return {
            'fd': connection.fd,            # always 0 on windows
            'family': str(connection.family),
            'type': connection.type,
            'laddr': addr(connection.laddr),
            'raddr': addr(connection.raddr),
            'status': connection.status,
            'pid': connection.pid
        }

    connections = psutil.net_connections(kind=kind)

    return [jsonify(c) for c in connections]


def net_if_addrs():
    def jsonify(addrs):
        def addr(a):
            if len(a):
                return { 'ip': a.ip, 'port': a.port }

        return [{
            'family': str(addr.family),
            'address': addr.address,
            'netmask': addr.netmask,
            'broadcast': addr.broadcast,
            'ptp': addr.ptp
        } for addr in addrs]

    if_addrs = psutil.net_if_addrs()
    json_addrs = {}

    for (name, addrs) in if_addrs.items():
        json_addrs[name] = jsonify(addrs)

    return json_addrs


def net_if_stats():
    def jsonify(stats):
        return {
            'isup': stats.isup,
            'duplex': str(stats.duplex),
            'speed': stats.speed,
            'mtu': stats.mtu
        }

    stats = psutil.net_if_stats()
    json_stats = {}

    for (name, s) in stats.items():
        json_stats[name] = jsonify(s)

    return json_stats


##############################################################


if __name__ == '__main__':
    processor()
