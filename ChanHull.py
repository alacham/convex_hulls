'''
Created on 13.11.2012

@author: jirka
'''
import math, random
from Tkinter import Tk, Canvas

LEFT,RIGHT,STRAIGHT = 1, -1, 0

COLORS = ("white", "black", "red", "green", "blue", "cyan", "yellow", "magenta")
UC = ("white", "black", "green", "cyan", "yellow", "magenta")


def turn_dir(p1,p2,p3):
    return cmp(vector_multip_determ(p1, p2, p3),0)

def p_dist(p1,p2):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

def vector_multip_determ(p1, p2, point):
    diag1 = (p2[0] - p1[0]) * (point[1] - p1[1])
    diag2 = (p2[1] - p1[1]) * (point[0] - p1[0])
    return diag1 - diag2

def is_3rd_left(p1,p2,p3):
    if vector_multip_determ(p1, p2, p3) > 0:
        return True
    return False

def is_3rd_right(p1,p2,p3):
    if vector_multip_determ(p1, p2, p3) < 0:
        return True
    return False

def left_tangent(hull, spoint):
#    print 'Hull:', hull, spoint
    l = 0
    r = len(hull)
    prev_d = turn_dir(spoint, hull[0], hull[-1])
    next_d = turn_dir(spoint, hull[0], hull[1])
    if prev_d != LEFT and next_d != LEFT:
        if prev_d == STRAIGHT:
            if p_dist(spoint, hull[0]) > p_dist(spoint, hull[-1]):
                return 0
            else: # not really sure if this can happen
                return r-1
        elif next_d == STRAIGHT:
            if p_dist(spoint, hull[0]) > p_dist(spoint, hull[1]):
                return 0
            else:
                return 1
        return 0
    
    _runindex = 0
    while l < r:
#        for p_i in range(l,r+1):
#            i = hull[p_i][0]
#            j = hull[p_i][1]
#            global w
#            w.create_oval(i-(2+_runindex),j-(2+_runindex),i+3+_runindex,j+3+_runindex,outline=UC[_runindex/2],width=1)
        
        new = (l+r)/2
        new_prev = turn_dir(spoint, hull[new], hull[new-1])
        new_next = turn_dir(spoint, hull[new], hull[(new+1)%len(hull)])
        with_l = turn_dir(spoint, hull[l], hull[new])
#        print new, with_l, new_prev, next_d
        if new_prev != LEFT and new_next != LEFT:
            if new_prev == STRAIGHT:
                if p_dist(spoint, hull[new]) > p_dist(spoint, hull[new-1]):
                    return new
                else: # not really sure if this can happen
                    return new-1
            elif new_next == STRAIGHT:
                if p_dist(spoint, hull[new]) > p_dist(spoint, hull[new+1]):
                    return new
                else:
                    return new+1
            return new
        elif (with_l == RIGHT and next_d == LEFT) or (with_l == LEFT and new_prev == LEFT):
            r = new
        else:
            l = new + 1
            prev_d = -new_next
            next_d = turn_dir(spoint,hull[l],hull[(l+1)%len(hull)])
            if prev_d != LEFT and next_d != LEFT:
                if prev_d == STRAIGHT:
                    if p_dist(spoint, hull[l]) > p_dist(spoint, hull[l-1]):
                        return l
                    else: # not really sure if this can happen
                        return l-1
                elif next_d == STRAIGHT:
                    if p_dist(spoint, hull[l]) > p_dist(spoint, hull[(l+1)%len(hull)]):
                        return l
                    else:
                        return l+1
                return l
#        _runindex += 2
    assert(False)
    return l
    


def graham_scan(inpoints):
    points = sorted(inpoints)
    hulls = ([],[])
    iters = (iter(points),reversed(points))
    for hull, piter in zip(hulls, iters):
        for i in piter:
            if len(hull) <= 1:
                hull.append(i)
            else:
                while len(hull) > 1 and not is_3rd_right(hull[-2], hull[-1],i):
                    hull.pop()
                hull.append(i)
    #return hulls[1] + hulls[0][1:-1] ## proti smeru rucicek
    return hulls[0] + hulls[1][1:-1] ## po smeru rucicek
    

def first_point(hulls):
    h_i,p_i = 0,0
    for i in xrange(len(hulls)):
        for j in xrange(len(hulls[i])):
            if hulls[i][j] < hulls[h_i][p_i]:
                h_i,p_i = i,j
    return h_i,p_i



def next_point(hulls, previous):
    h,p = previous
    last_p = hulls[h][p]
    n_h, n_p = h, (p+1)%len(hulls[h])
    next_p = hulls[h][n_p]
    for h_i in xrange(len(hulls)):
        if h_i == h:
            continue
        p_i = left_tangent(hulls[h_i], last_p)
        point = hulls[h_i][p_i]
        turn = turn_dir(last_p, next_p, point)
        if turn==LEFT or (turn == STRAIGHT and p_dist(last_p, next_p) < p_dist(last_p, point)):
            n_h, n_p = h_i, p_i
            next_p = hulls[n_h][n_p]
    return n_h, n_p

def hull_attempt(hulls, maxnum):
    whole_hull = [ first_point(hulls)]
    while len(whole_hull) < maxnum:
        whole_hull.append(next_point(hulls, whole_hull[-1]))
        if whole_hull[0] == whole_hull[-1]:
            break
    return whole_hull


def chan_hull(pointlist):
    t = 0
    while True:
        t += 1
        num = min(2**(2**t),len(pointlist))
        subhulls = []
        for i in xrange(0,len(pointlist),num):
            newhull = graham_scan(pointlist[i:i+num])
            subhulls.append(newhull)
        whole_hull = hull_attempt(subhulls, num)
        if whole_hull[0] == whole_hull[-1]:
            return map(lambda x: subhulls[x[0]][x[1]],whole_hull)[:-1]
        


    
if __name__ == '__main__':
    random.seed((0,0))
    

    if True:
        hlavni = Tk()
        w = Canvas(hlavni, width=800, height=800)
        w.pack()
        
        
        points = list(set([(random.randint(50,750),random.randint(50,750)) for i in range(0,1000)])) #get rid of duplicities
        random.shuffle(points)
        
        print 'gscan:',graham_scan(points)
        import QuickHull
        print 'qhull:',QuickHull.quick_hull(set(points))
        
        hull = chan_hull(points)
        
        print hull
        
        hullpargs = reduce(lambda x,y: x + list(y), hull, [])

        w.create_polygon(*hullpargs,fill='',width=1,outline='red')
#        for i in tangents:
#            w.create_line(*i,fill='blue',dash=(3,15))
        hlavni.mainloop()
        
        
        