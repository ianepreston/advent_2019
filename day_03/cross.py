import re


def readpaths(filename):
    with open(filename, "r") as f:
        return [line.split(",") for line in f.readlines()]


def delta(direction):
    rgx = r"([A-Z])([0-9]+)"
    match = re.match(rgx, direction)
    move, num = match.groups()
    num = int(num)
    dir_dict = {"L": (-num, 0), "R": (num, 0), "U": (0, num), "D": (0, -num)}
    return dir_dict[move]


def manhattan_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist


def line_seg(start_point, move):
    xs, ys = start_point
    dx, dy = move
    if dx < 0 or dy < 0:
        step = -1
    else:
        step = 1
    if dx != 0:
        seg = [(x, ys) for x in range(xs, dx + step, step)]
    else:
        seg = [(xs, y) for y in range(ys, dy + step, step)]
    return seg

def fullseg(moves):
    xs = ys = 0
    points = set()
    for move in moves:
        seg = line_seg((xs, ys), move)
        for point in seg:
            points.add(point)
        xs, ys = seg[-1]
    points.remove((0, 0))
    return points

def intersections(points1, points2):
    return points1.intersection(points2)

def part1