'''
Created on 13.11.2012

@author: jirka
'''
import math, random
from Tkinter import Tk, Canvas

from utils import *

LEFT,RIGHT,STRAIGHT = 1, -1, 0

COLORS = ("white", "black", "red", "green", "blue", "cyan", "yellow", "magenta")
UC = ("white", "black", "green", "cyan", "yellow", "magenta")


def pos2point(pos,hulls):
    return hulls[pos[0]][pos[1]]

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

def left_tangent(hull, spoint, animqueue):
    l = 0
    r = len(hull)
    prev_d = turn_dir(spoint, hull[0], hull[-1])
    next_d = turn_dir(spoint, hull[0], hull[1])
    animqueue.append(('point_line', 'left', CURRPOINT, [spoint,hull[0]],dict(width=3,dash=(5,5),dashoffset=0)))
    animqueue.append(('point_line', 'right', PROCESSEDPOINT, [spoint,hull[0]],dict(width=3,dash=(5,5),dashoffset=4)))
    animqueue.append(('point', 'center', PROCESSEDPOINT, (-10,-10))) ## something to have delete when returns early
    
    if prev_d != LEFT and next_d != LEFT:
        animqueue.append(('step'))
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
    animqueue.append(('remove', 'center'))
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
        
        animqueue.append(('step'))
        animqueue.append(('point_line', 'center', GREENGOOD, [spoint,hull[new]],dict(width=2,dashoffset=4)))
        animqueue.append(('step'))
#        print new, with_l, new_prev, next_d
        if new_prev != LEFT and new_next != LEFT: #new "pivot" is the tangent point
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
            animqueue.append(('remove', 'right'))
            animqueue.append(('point_line', 'right', PROCESSEDPOINT, [spoint,hull[r]],dict(width=3,dash=(5,5),dashoffset=4)))
            animqueue.append(('step'))
        else:
            l = new + 1
            animqueue.append(('remove', 'left'))
            animqueue.append(('point_line', 'left', CURRPOINT, [spoint,hull[l]],dict(width=3,dash=(5,5),dashoffset=4)))
            animqueue.append(('step'))
            
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
        animqueue.append(('remove', 'center'))
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



def next_point(hulls, previous, animqueue):
    h,p = previous
    last_p = hulls[h][p]
    n_h, n_p = h, (p+1)%len(hulls[h])
    next_p = hulls[h][n_p]
    animqueue.append(('hull', str(id(hulls[h])), UPHULL, hulls[h],dict(width=3)))
    animqueue.append(('point_line', 'currnext', OUTLINE, (last_p, next_p),dict(width=3)))
    animqueue.append(('step'))
    animqueue.append(('remove', str(id(hulls[h]))))
    animqueue.append(('remove', id(hulls[h])))
    animqueue.append(('hull', id(hulls[h]), LOHULL, hulls[h],dict(dash=(5,5),width=1)))
    
    for h_i in xrange(len(hulls)):
        if h_i == h:
            continue
        animqueue.append(('hull', str(id(hulls[h_i])), UPHULL, hulls[h_i],dict(width=3)))
        p_i = left_tangent(hulls[h_i], last_p, animqueue)
        animqueue.append(('step'))
        animqueue.append(('remove', 'right'))
        animqueue.append(('remove', 'center'))
        animqueue.append(('remove', 'left'))
        animqueue.append(('remove', str(id(hulls[h_i]))))
        animqueue.append(('remove', id(hulls[h_i])))
        animqueue.append(('hull', id(hulls[h_i]), LOHULL, hulls[h_i],dict(dash=(5,5),width=1)))
        point = hulls[h_i][p_i]
        animqueue.append(('point_line', 'candidate', BLUEDUNNO, (last_p, point),dict(width=3)))
        animqueue.append(('step'))
        turn = turn_dir(last_p, next_p, point)
        if turn==LEFT or (turn == STRAIGHT and p_dist(last_p, next_p) < p_dist(last_p, point)):
            animqueue.append(('remove', 'currnext'))
            animqueue.append(('remove', 'candidate'))
            animqueue.append(('point_line', 'currnext', REDBAD, (last_p, next_p),dict(width=3)))
            animqueue.append(('point_line', 'candidate', GREENGOOD, (last_p, point),dict(width=3)))
            animqueue.append(('step'))
            n_h, n_p = h_i, p_i
            next_p = hulls[n_h][n_p]
            animqueue.append(('remove', 'currnext'))
            animqueue.append(('remove', 'candidate'))
            animqueue.append(('point_line', 'currnext', OUTLINE, (last_p, next_p),dict(width=3)))
        else:
            animqueue.append(('remove', 'candidate'))
            animqueue.append(('point_line', 'candidate', REDBAD, (last_p, point),dict(width=3)))
            animqueue.append(('remove', 'currnext'))
            animqueue.append(('point_line', 'currnext', GREENGOOD, (last_p, next_p),dict(width=3)))
            animqueue.append(('step'))
            animqueue.append(('remove', 'currnext'))
            animqueue.append(('remove', 'candidate'))
            animqueue.append(('point_line', 'currnext', OUTLINE, (last_p, next_p),dict(width=3)))
    animqueue.append(('remove', 'currnext'))
    return n_h, n_p

def hull_attempt(hulls, maxnum, animqueue):
    whole_hull = [ first_point(hulls)]
    
    animqueue.append(('point', 'p1', PROCESSEDPOINT, pos2point(whole_hull[0],hulls),dict(width=3)))
    
    animqueue.append(('step'))
    while len(whole_hull) < maxnum:
        animqueue.append(('point_line', 'currattempt', OUTLINE, map(lambda x: hulls[x[0]][x[1]],whole_hull),dict(width=3)))
        animqueue.append(('text', 'subcounter', REDBAD, str(len(whole_hull)),(20,35)))
        animqueue.append(('step'))
        whole_hull.append(next_point(hulls, whole_hull[-1], animqueue))
        ## drawshit only inside loop
        for h_i in range(len(hulls)):
            animqueue.append(('remove', id(hulls[h_i])))
            animqueue.append(('hull', id(hulls[h_i]), LOHULL, hulls[h_i]))
        
        if whole_hull[0] == whole_hull[-1]:
            animqueue.append(('point_line', 'currattempt', OUTLINE, map(lambda x: hulls[x[0]][x[1]],whole_hull),dict(width=3)))
            break
        animqueue.append(('remove', 'currattempt'))
        animqueue.append(('remove', 'subcounter'))
    return whole_hull


def chan_hull(pointlist, animqueue):
    t = 0
    animqueue.append(('text', 'chancounter', PROCESSEDPOINT, str(t),(20,20)))
    while True:
        t += 1
        num = min(2**(2**t),len(pointlist))
        animqueue.append(('remove', 'chancounter'))
        animqueue.append(('text', 'chancounter', PROCESSEDPOINT, str(num),(20,20)))
        subhulls = []
        for i in xrange(0,len(pointlist),num):
            newhull = graham_scan(pointlist[i:i+num])
            animqueue.append(('hull', id(newhull), LOHULL, newhull))
            subhulls.append(newhull)
        whole_hull = hull_attempt(subhulls, num, animqueue)
        if whole_hull[0] == whole_hull[-1]:
            return map(lambda x: subhulls[x[0]][x[1]],whole_hull)[:-1]
        
        animqueue.append(('step'))
        for i in subhulls:
            animqueue.append(('remove', id(i)))
        


    
if __name__ == '__main__':
    random.seed((0,0))
    

    hlavni = Tk()
    w = Canvas(hlavni, width=800, height=800)
    w.pack()
    
    
    points = list(set([(random.randint(50,750),random.randint(50,750)) for i in range(0,200)])) #get rid of duplicities
    random.shuffle(points)
    
    tkinterpoints = {}    
    for point in points:
        tkinterpoints[point] = w.create_oval(point[0],point[1],point[0],point[1],width=1)
    
    aqueue = []
    hull = chan_hull(points, aqueue)
    
    

    ddict = {}
    def do_something(tkintevent):
        draw_queue_step(w,aqueue, ddict)
        
    def skip_something(tkintevent):
        for i in range(50):
            draw_queue_step(w,aqueue, ddict)

    w.bind('<Button-1>', do_something)
    w.bind('<Button-3>', skip_something)
    
#        hullpargs = reduce(lambda x,y: x + list(y), hull, [])
#        w.create_polygon(*hullpargs,fill='',width=1,outline='red')
#        for i in tangents:
#            w.create_line(*i,fill='blue',dash=(3,15))
    hlavni.mainloop()
    
    
    
