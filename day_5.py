#!/usr/bin/python3

from re import finditer, match
from re import compile as regex_compile
from utilities.argparse_and_time import arparse_and_time_wrapper, SETDAY

SETDAY(5)

SEED_PATTERN = regex_compile(r'\s*seeds:\s*((\d+\s?)*)')
MAP_PATTERN = regex_compile(r'\s*([a-z]+)-to-([a-z]+) map:\n((\d+\s\d+\s\d+\n)*)')
VALUE_PATTERN = regex_compile(r'(\d+)\s+(\d+)\s+(\d+)')

class Range():
    def __init__(self):
        self.start = None
        self.end = None

    def from_runlength(self, s, l):
        if l <= 0:
            return None
        self.start = s
        self.end = s + l
        return self

    def from_start_end(self, s, e):
        if e-s <= 0:
            return None
        self.start = s
        self.end = e
        return self

    def __repr__(self):
        return f'({self.start}..{self.end-1})'

    def get_runlength(self):
        return self.start, self.end-self.start

    def get_start_end(self):
        return self.start, self.end

    def intersection(self, other):
        before = inside = after = None
        r = Range().from_start_end(self.start, self.end)

        if r.start < other.start:
            before = Range().from_start_end(r.start, other.start)
            r = Range().from_start_end(other.start, r.end)
        if r is None:
            return before, inside, after

        if r.start < other.end:
            inside = Range().from_start_end(r.start, min(r.end, other.end))
            r = Range().from_start_end(other.end, r.end)
        if r is None:
            return before, inside, after

        after = r
        return before, inside, after

    def offset(self, d):
        self.start += d
        self.end += d
        return self


class RangeMap():
    def __init__(self):
        self.ranges = []
        self.is_sorted = True

    def add_range(self, sstart, dstart, length):
        self.ranges += [ (sstart, dstart, length) ]
        self.is_sorted = False
        return self

    def __repr__(self):
        return str(self.ranges)

    def resort(self):
        self.ranges.sort(key=lambda x: x[0])
        return self

    def __getitem__(self, key):
        if isinstance(key, int):
            for range_ in self.ranges:
                if range_[0] <= key < range_[0] + range_[2]:
                    return range_[1] + (key - range_[0])
            return key
        else:
            return_ranges = []
            if not self.is_sorted:
                self.resort()
            s = Range().from_runlength(key[0], key[1])
            for range_ in self.ranges:
                r = Range().from_runlength(range_[0], range_[2])
                before, inside, after = s.intersection(r)
                if before is not None:
                    return_ranges.append(before.get_runlength())
                if inside is not None:
                    d = range_[1] - range_[0]
                    inside = inside.offset(d)
                    return_ranges.append(inside.get_runlength())
                if after is None:
                    return return_ranges
                s = after
            return_ranges.append(s.get_runlength())
            return return_ranges

def minimize_set_of_ranges(r):
    #r = list(r)
    r.sort(key=lambda x: x[0])
    r = [Range().from_runlength(*p) for p in r]
    w = [r[0]]
    for i, t in enumerate(r[:-1]):
        a, b, c = t.intersection(r[i+1])
        if (b is not None) or (t.end == r[i+1].start):
            # Merge
            w[-1] = Range().from_start_end(w[-1].start, r[i+1].end)
        else:
            w.append(r[i+1])
    return [m.get_runlength() for m in w]


def solve(input_: str, flags: dict) -> int:
    answer = 0
    seed_match = SEED_PATTERN.match(input_)
    seeds = [int(seed) for seed in seed_match.group(1).split(' ')]
    if flags['fix']:
        seeds_new = []
        f = 0
        for i, seed in enumerate(seeds):
            if not i%2:
                f = seed
            else:
                seeds_new.append( (f, seed) )
        seeds = seeds_new
    input_ = input_[seed_match.end():]
    maps = []
    for map_match in MAP_PATTERN.finditer(input_):
        source = map_match.group(1)
        dest = map_match.group(2)
        new_map = RangeMap()

        for range_str in VALUE_PATTERN.finditer(map_match.group(3)):
            drange = int(range_str.group(1))
            srange = int(range_str.group(2))
            length = int(range_str.group(3))
            new_map.add_range(srange, drange, length)
        maps.append( (source, dest, new_map) )

    if not flags['fix']:
        for map_ in maps:
            seeds = [map_[2][seed] for seed in seeds]
    else:
        for map_ in maps:
            ranges = [map_[2][seed] for seed in seeds]
            seeds = []
            for range_ in ranges:
                seeds += range_
            seeds = minimize_set_of_ranges(seeds)
        seeds = [seed[0] for seed in seeds]

    return min(seeds)


if __name__ == '__main__':
    solve = arparse_and_time_wrapper(solve)
    solve()
