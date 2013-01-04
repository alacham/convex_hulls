'''
Created on 12.10.2012

@author: jirka
'''
import math
import random
from utils import *


def signum(x):
    return cmp(x,0)

def vector_multip_determ(p1, p2, point):
    diag1 = (p2[0] - p1[0]) * (point[1] - p1[1])
    diag2 = (p2[1] - p1[1]) * (point[0] - p1[0])
    return diag1 - diag2

def inside_triangle(p1,p2,p3,testpoint):
    a = signum(vector_multip_determ(p1,p2,testpoint))
    b = signum(vector_multip_determ(p2,p3,testpoint))
    c = signum(vector_multip_determ(p3,p1,testpoint))
    s = a + b + c
    if s >= 2 or s <= -2:
        return True
    return False

def is_3_out(p0, p1, p2, is_upper=True):
    if p0 < p1:
        determ = vector_multip_determ(p0, p1, p2)
    else:
        determ = vector_multip_determ(p1, p0, p2)
    if (is_upper and determ > 0) or (not is_upper and determ < 0):
        return True
    return False


def recurrent_qhull(lm, rm, plist, animqueue,is_upper=True):
    if not plist:
        return []
    line = (lm, rm)
    most_distant = max(plist, key=lambda x: geoPointLineDist(x, line, testSegmentEnds=False))
    animqueue.append(('point', 'p'+str(most_distant), PROCESSEDPOINT, most_distant,dict(width=2)))
    animqueue.append(('hull', str(lm)+str(rm)+str(most_distant), BLUEDUNNO, [lm,rm,most_distant],dict(width=2,dash=(5,5),dashoffset=3,fill='black')))
    animqueue.append(('step'))
    
    lhull = set()
    rhull = set()
    for pi in plist:
        if is_3_out(lm, most_distant, pi, is_upper):
            lhull.add(pi)
        elif is_3_out(most_distant, rm, pi, is_upper):
            rhull.add(pi)
    
    return recurrent_qhull(lm, most_distant, lhull, animqueue,is_upper) + [most_distant] +\
        recurrent_qhull(most_distant, rm, rhull, animqueue,is_upper)

    


def geoPointLineDist(p, seg, testSegmentEnds=False):
    """
    Minimum Distance between a Point and a Line
    Written by Paul Bourke,    October 1988
    http://astronomy.swin.edu.au/~pbourke/geometry/pointline/
    
    ruthlessly stolen from:
    https://priithon.googlecode.com/hg/Priithon/usefulGeo.py
    """

    x3, y3 = p
    (x1, y1), (x2, y2) = seg

    dx21 = (x2 - x1)
    dy21 = (y2 - y1)
    
    lensq21 = dx21 * dx21 + dy21 * dy21
    if lensq21 == 0:
        #20080821 raise ValueError, "zero length line segment"
        dy = y3 - y1 
        dx = x3 - x1 
        return math.sqrt(dx * dx + dy * dy)  # return point to point distance

    u = (x3 - x1) * dx21 + (y3 - y1) * dy21
    u = u / float(lensq21)


    x = x1 + u * dx21
    y = y1 + u * dy21    

    if testSegmentEnds:
        if u < 0:
            x, y = x1, y1
        elif u > 1:
            x, y = x2, y2
    

    dx30 = x3 - x
    dy30 = y3 - y

    return math.sqrt(dx30 * dx30 + dy30 * dy30)





def quick_hull(points, animqueue):
    '''
    Constructor
    '''
    pointSet = points
    lmost = min(points)
    rmost = max(points)
    
    pointSet.discard(lmost)
    pointSet.discard(rmost)

    uhull = []
    dhull = []
    for point in pointSet:
        if is_3_out(lmost, rmost, point, is_upper=True):
            uhull.append(point)
        elif is_3_out(lmost, rmost, point, is_upper=False):
            dhull.append(point)
            
    animqueue.append(('point', 'p'+str(lmost), PROCESSEDPOINT, lmost,dict(width=2)))
    animqueue.append(('point', 'p'+str(rmost), PROCESSEDPOINT, rmost,dict(width=2)))
    animqueue.append(('point_line', str(lmost)+str(rmost), BLUEDUNNO, [lmost,rmost],dict(width=1.4,dash=(5,5),dashoffset=3)))
    animqueue.append(('step'))
    
    hull = [lmost] + recurrent_qhull(lmost, rmost, uhull, animqueue,is_upper= True) +\
        [rmost] + list(reversed(recurrent_qhull(lmost, rmost, dhull, animqueue,is_upper= False)))
    return hull

        
        
if __name__ == '__main__':
    from Tkinter import Tk, Canvas
    hlavni = Tk()
    w = Canvas(hlavni, width=800, height=800)
    w.pack()
    pointlist = set([(random.randint(50,750),random.randint(50,750)) for i in range(100)])
    for point in pointlist:
        w.create_oval(point[0],point[1],point[0],point[1],width=1)
    
    animqueue = []
    qh = quick_hull(pointlist,animqueue)
    animqueue.append(('step'))
    animqueue.append(('hull', 'full', GREENGOOD, qh,dict(width=3)))
    animqueue.append(('points', 'all', GREENGOOD, qh,dict(width=3)))
    
    #w.create_polygon(*hullpargs,fill='',width=1,outline='red')
    
    ddict = {}
    
    def do_something(tkintevent):
        draw_queue_step(w,animqueue, ddict)

    w.bind('<Button-1>', do_something)
    
    hlavni.mainloop()
