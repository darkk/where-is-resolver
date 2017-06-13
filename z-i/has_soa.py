#!/usr/bin/python2 

import sys
import multiprocessing.dummy as mp

import dns.resolver
import dns.exception

def get_soa(fqdn):
    fqdn = fqdn.strip('.')
    root = '.'.join(fqdn.rsplit('.', 2)[-2:])
    resolver = dns.resolver.get_default_resolver()
    for i in xrange(4):
        try:
            return resolver.query(root, 'SOA'), None
        except dns.exception.Timeout:
            pass
        except Exception, exc:
            return None, exc


def main():
    dns.resolver.get_default_resolver() # init
    p = mp.Pool(16)
    domains = [_.strip() for _ in sys.stdin]
    result = p.map(get_soa, domains)
    for fqdn, (answer, err) in zip(domains, result):
        if answer is not None:
            print fqdn, ' '.join(str(_) for _ in answer)

if __name__ == '__main__':
    main()
