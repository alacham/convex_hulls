# Chan's Convex Hull O(n log h) - Tom Switzer <thomas.switzer@gmail.com>

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

def turn(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

def _keep_left(hull, r):
    while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
            hull.pop()
    return (not len(hull) or hull[-1] != r) and hull.append(r) or hull

def _rtangent(hull, p):
    """Return the index of the point in hull that the right tangent line from p
to hull touches.
"""
    l, r = 0, len(hull)
    l_prev = turn(p, hull[0], hull[-1])
    l_next = turn(p, hull[0], hull[(l + 1) % r])
    while l < r:
        c = (l + r) / 2
        c_prev = turn(p, hull[c], hull[(c - 1) % len(hull)])
        c_next = turn(p, hull[c], hull[(c + 1) % len(hull)])
        c_side = turn(p, hull[l], hull[c])
        print c, hull[c], c_prev, c_next
        if c_prev != TURN_RIGHT and c_next != TURN_RIGHT:
            return c
        elif c_side == TURN_LEFT and (l_next == TURN_RIGHT or
                                      l_prev == l_next) or \
                c_side == TURN_RIGHT and c_prev == TURN_RIGHT:
            r = c # Tangent touches left chain
        else:
            l = c + 1 # Tangent touches right chain
            l_prev = -c_next # Switch sides
            l_next = turn(p, hull[l], hull[(l + 1) % len(hull)])
    return l

mh = [(0, 1), (1, 0), (2, 0), (3, 1), (2, 2), (1, 2)]
print _rtangent(mh,(4,0))
