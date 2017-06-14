#!/usr/bin/env python

import sys
import json

def compare(test, ctrl):
    l = zip(test['result'], ctrl['result'])
    it = iter(l)
    for t, c in it:
        test_ip = {_.get('from') for _ in t['result']}
        test_ip.discard(None)
        ctrl_ip = {_.get('from') for _ in c['result']}
        ctrl_ip.discard(None)
        if test_ip != ctrl_ip:
            # both this and next hop is non-terminal
            if all([_.get('flags') is None for _ in (c['result'] + t['result'])]):
                pair = next(it, None)
                if pair:
                    t, c = pair
                    if all([_.get('flags') is None for _ in (c['result'] + t['result'])]):
                        print json.dumps({'prb_id': test['prb_id'], 'test': t, 'ctrl': c})
            return

def main():
    cache = {}
    for fname in sys.argv[1:]:
        with open(fname) as fd:
            for line in fd:
                doc = json.loads(line)
                key = doc['prb_id']
                pair = cache.get(key)
                if pair is not None:
                    compare(doc, pair)
                    del cache[key]
                else:
                    cache[key] = doc

if __name__ == '__main__':
    main()
