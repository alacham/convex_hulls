
from ChanHull import graham_scan
from QuickHull import quick_hull

import math, random, sys
from Tkinter import Tk, Canvas


from utils import *


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

def to_sorted_tuple(lst):
    return sorted(lst)


def DivideHull2D(inpoints, lp, rp, animqueue, lower=False):
    alen = len(animqueue) ## should solve problem with same names
    
    print 'descent'
    points_c = []
    
    
    aqueue.append(('point', 'pleft', REDBAD, lp, dict(width=2.5)))
    aqueue.append(('point', 'pright', GREENGOOD, rp, dict(width=2.5)))
    animqueue.append(('point_line', 'upperdowner', BLACK, (lp,rp),dict(width=2)))
    animqueue.append('step')
    for p in inpoints:
        if not lower:
            if is_3rd_left(lp, rp, p):
                points_c.append(p)
            else:
                animqueue.append(('remove', str(p)+str(lower)))
                pass
        else:
            if is_3rd_right(lp, rp, p):
                points_c.append(p)
            else:
                animqueue.append(('remove', str(p)+str(lower)))
                pass
    animqueue.append('step')
    animqueue.append(('remove', 'upperdowner'))
    print lp, rp, points_c
    if not points_c:
        aqueue.append(('remove', 'pleft'))
        aqueue.append(('remove', 'pright'))
        aqueue.append(('point', 'hull'+str(lp), YELLOW, lp, dict(width=2.7)))
        aqueue.append(('point', 'hull'+str(lp), YELLOW, rp, dict(width=2.7)))
        return [lp,rp]
    if len(points_c) == 1:
        aqueue.append(('remove', 'pleft'))
        aqueue.append(('remove', 'pright'))
        aqueue.append(('point', 'hull'+str(lp), YELLOW, lp, dict(width=2.7)))
        aqueue.append(('point', 'hull'+str(lp), YELLOW, rp, dict(width=2.7)))
        aqueue.append(('point', 'hull'+str(points_c[0]), YELLOW, points_c[0], dict(width=2.7)))
        return [lp, points_c[0], rp]
    
    random.shuffle(points_c)
    
    # this should be done in linear time
    lines = [ sorted(points_c[2*i:2*i+2])  for i in xrange(0,len(points_c)/2)]
    points2 = reduce(lambda x,y: x + list(y), lines, [])
    if len(points_c) % 2 == 1:
        points2.append(points_c[-1])
    points_c = points2
    
    ## drawing shit
    for l in lines:
        animqueue.append(('point_line', str(l), WHITE, l,dict(width=2)))
    animqueue.append('step')
    
    slopes = []
    ind = 0
    for l in lines:
        slope = (l[1][1]-l[0][1])/(l[1][0]*1.0-l[0][0])
        slopes.append((slope,ind))
        ind += 1
    sslopes = sorted(slopes)
    median = sslopes[len(sslopes)/2]
    
    animqueue.append(('point_line', 'median', BLUEDUNNO, lines[median[1]],dict(width=3)))
    animqueue.append('step')

    
    pmax = points_c[0]
    for i in points_c + [lp,rp]:
        if not lower:
            if (i[1] - median[0] * i[0]) > (pmax[1] - median[0] * pmax[0]):
                pmax = i
        else:
            if (i[1] - median[0] * i[0]) < (pmax[1] - median[0] * pmax[0]):
                pmax = i
    #pmax = max(points_c + [lp,rp], key=lambda x: x[1] - median[0] * x[0])
    
    aqueue.append(('point', 'pmax', BLUEDUNNO, pmax, dict(width=2.5)))
    animqueue.append('step')
    animqueue.append(('point_line', 'divider'+str((lp,rp,alen)), BLACK, [(pmax[0],0),(pmax[0],800)],dict(width=2, dash=(5,5))))
    animqueue.append('step')
    aqueue.append(('remove', 'pmax'))
    animqueue.append(('remove', 'median'))
    for l in lines:
        animqueue.append(('remove', str(l)))
    
    for l_i in range(len(lines)):
        if slopes[l_i][0] == median[0]:
            animqueue.append(('point_line', str(lines[l_i]), BLUEDUNNO, lines[l_i],dict(width=2)))
        elif slopes[l_i][0] > median[0]:
            animqueue.append(('point_line', str(lines[l_i]), BROWN, lines[l_i],dict(width=2)))
        else:
            animqueue.append(('point_line', str(lines[l_i]), ORANGE, lines[l_i],dict(width=2)))
    animqueue.append('step')
    
    anim_todelete = [] 

    
    points_left = []
    points_right = []
    ind = 0
    for p in points_c:
        if not lower: # upper hull
            if p[0] < pmax[0]:
                if ind%2 == 1 and slopes[ind/2]<=median:
                    animqueue.append(('remove', str(p)+str(lower)))
                    aqueue.append(('point', 'td'+str(p), REDBAD, p, dict(width=3)))
                    anim_todelete.append('td'+str(p))
                    pass
                else:
                    points_left.append(p)
            elif p[0] > pmax[0]:
                if ind%2 == 0 and ind!=(len(points_c)-1) and slopes[ind/2]>=median:
                    animqueue.append(('remove', str(p)+str(lower)))
                    aqueue.append(('point', 'td'+str(p), REDBAD, p, dict(width=3)))
                    anim_todelete.append('td'+str(p))
                    pass
                else:
                    points_right.append(p)
        else: # bottom hull
            if p[0] < pmax[0]:
                if ind%2 == 1 and slopes[ind/2]>=median:
                    animqueue.append(('remove', str(p)+str(lower)))
                    aqueue.append(('point', 'td'+str(p), REDBAD, p, dict(width=3)))
                    anim_todelete.append('td'+str(p))
                    pass
                else:
                    points_left.append(p)
            elif p[0] > pmax[0]:
                if ind%2 == 0 and ind!=(len(points_c)-1) and slopes[ind/2]<=median:
                    animqueue.append(('remove', str(p)+str(lower)))
                    aqueue.append(('point', 'td'+str(p), REDBAD, p, dict(width=3)))
                    anim_todelete.append('td'+str(p))
                    pass
                else:
                    points_right.append(p)
        ind += 1
    animqueue.append('step')
    for l in lines:
        animqueue.append(('remove', str(l)))
    for i in anim_todelete:
        animqueue.append(('remove', str(i)))
    
    animqueue.append('step')
    aqueue.append(('remove', 'pleft'))
    aqueue.append(('remove', 'pright'))
    
    if pmax == lp:
        retval = DivideHull2D(points_right, lp, rp, animqueue, lower)
    elif pmax == rp:
        retval = DivideHull2D(points_left, lp, rp, animqueue, lower)
    else:
        retval1 = DivideHull2D(points_left, lp, pmax, animqueue, lower)
        
        retval2 = DivideHull2D(points_right, pmax, rp, animqueue, lower)
        
        retval = retval1 + retval2
    
    animqueue.append(('remove', 'divider'+str((lp,rp,alen))))
    animqueue.append('step')
    #print 'return', retval
    return retval

def chan_hull2(inpoints, animqueue):
    points = inpoints[:]
    lpi = min(xrange(len(points)), key=lambda x:points[x])
    lp = points[lpi]
    points.pop(lpi)
    
    rpi = max(xrange(len(points)), key=lambda x:points[x])
    rp = points[rpi]
    points.pop(rpi)
    
    upper_hull = DivideHull2D(points, lp, rp, animqueue, lower=False)
    animqueue.append(('step'))
    bottom_hull = DivideHull2D(points, lp, rp, animqueue, lower=True)
    bottom_hull.reverse()
    animqueue.append(('step'))
    whole_hull = [upper_hull[0]]
    for i in upper_hull + bottom_hull:
        if i != whole_hull[-1] and i != whole_hull[0]:
            whole_hull.append(i)
    animqueue.append(('hull','wholehull',YELLOW,whole_hull,dict(width=2)))
    return whole_hull
        




if __name__ == '__main__':
    #random.seed(1)
    points = [(random.randint(30,750),random.randint(50,730)) for i in range(0,500)]
    
    # i want unique values of x 
    points.sort()
    points2 = [points[0]]
    for i in points:
        if i[0] == points2[-1][0]:
            continue
        points2.append(i)
    points = points2
    random.shuffle(points)

    hlavni = Tk()
    w = Canvas(hlavni, width=800, height=800)
    w.pack()
    
    aqueue = []
    tkinterpoints = {}
    
    for point in points:
        tkinterpoints[point] = w.create_oval(point[0],point[1],point[0],point[1],width=1)
        aqueue.append(('point', str(point)+str(True), CYAN, point, dict(width=1.1, fill=CYAN)))
        aqueue.append(('point', str(point)+str(False), MAG, point, dict(width=1.5)))
    aqueue.append(('step'))
    
#    print '--------------------------------------'
    print chan_hull2(points,aqueue)
    
    ddict = {}
    def do_something(tkintevent):
        draw_queue_step(w,aqueue, ddict)
        
    def skip_something(tkintevent):
        for i in range(50):
            draw_queue_step(w,aqueue, ddict)

    w.bind('<Button-1>', do_something)
    w.bind('<Button-3>', skip_something)
    
    hlavni.mainloop()
    
    
    
    
    