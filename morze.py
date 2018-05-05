#!/usr/bin/env python3 

DIGRES = '-.. .. --. .. - .- .-.. .-. . ... .. ... - .- -. -.-. .' # digitalresistance

D0 = '-----'
D1 = '.----'
D2 = '..---'
D3 = '...--'
D4 = '....-'
D5 = '.....'
D6 = '-....'
D7 = '--...'
D8 = '---..'
D9 = '----.'

VP = '.-- --- .. ... - .. -. ..-  .--. --- .--. --- .-- --..-- ..-.-' # Voistinu popov!<FIN>

def iter_msg(msg, start=0, step=1):
    ts = start
    for c in msg:
        if c == '-':
            for i in range(3):
                yield (ts, 1)
                ts += step
            yield (ts, 0)
            ts += step
        elif c == '.':
            yield (ts, 1)
            ts += step
            yield (ts, 0)
            ts += step
        elif c == ' ':
            for i in range(2): # not `range(3)` as there is one `gap` from perv char
                yield (ts, 0)
                ts += step
        else:
            raise RuntimeError('Unknown char', c)

def main():
    step = 600
    #for ts, val in iter_msg(DIGRES, 1525473000, step):
    #    print('{{start={:d}, fin={:d}, value={:d}}},'.format(ts, ts+step, val))

    for ts, val in iter_msg(' '.join([D5, D4, D3, D2, D1, D0, VP]), 1525569600, step):
        print('{{start={:d}, fin={:d}, value={:d}}},'.format(ts, ts+step, val))

if __name__ == '__main__':
    main()
