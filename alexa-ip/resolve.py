#!/usr/bin/env python

from Queue import Queue
import itertools
import json
import socket
import sqlite3
import sys
import threading

NTHREADS = 128
EOF = object()

def write(qwrite, dbname):
    db = sqlite3.connect(dbname)
    while True:
        with db:
            c = db.cursor()
            task = qwrite.get()
            qwrite.task_done()
            if task is EOF:
                break
            rank, domain, af, gai = task
            table = {socket.AF_INET: 'ipv4', socket.AF_INET6: 'ipv6'}[af]
            c.execute('INSERT INTO {} VALUES (?, ?)'.format(table), [rank, gai])

def resolve(qresolv, qwrite):
    while True:
        task = qresolv.get()
        qresolv.task_done()
        if task is EOF:
            break
        (rank, domain), af = task
        try:
            gai = socket.getaddrinfo(domain, 0, af, socket.SOCK_STREAM)
        except Exception:
            gai = []
        gai = json.dumps([_[4][0] for _ in gai])
        qwrite.put((rank, domain, af, gai))

def main():
    qresolv = Queue(maxsize=65536)
    qwrite = Queue(maxsize=65536)
    while True:
        db = sqlite3.connect(sys.argv[1])
        with db:
            c = db.cursor()
            c.execute('SELECT rank, domain FROM domain WHERE rank NOT IN (SELECT rank FROM ipv4) LIMIT 10000')
            ipv4 = list(c)
            c.execute('SELECT rank, domain FROM domain WHERE rank NOT IN (SELECT rank FROM ipv6) LIMIT 10000')
            ipv6 = list(c)
        del db
        if not ipv4 and not ipv6:
            break
        writer = threading.Thread(target=write, args=(qwrite, sys.argv[1]))
        writer.start()
        resolver = [threading.Thread(target=resolve, args=(qresolv, qwrite)) for _ in xrange(NTHREADS)]
        for _ in resolver:
            _.start()
        for dom4, dom6 in itertools.izip_longest(ipv4, ipv6):
            if dom4 is not None:
                qresolv.put((dom4, socket.AF_INET))
            if dom6 is not None:
                qresolv.put((dom6, socket.AF_INET6))
        for _ in resolver:
            qresolv.put(EOF)
        for _ in resolver:
            _.join()
        qwrite.put(EOF)
        writer.join()

if __name__ == '__main__':
    main()
