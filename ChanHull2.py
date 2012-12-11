


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

def to_sorted_tuple(lst):
    return sorted(lst)


def DivideHull2D(inpoints, lp, rp, lower=False):
    points_c = []
    for p in inpoints:
        if is_3rd_left(lp, rp, p):
            points_c.append(p)
        
    if not points_c:
        return sorted([lp, rp],reverse=lower)
    if len(points_c) == 1:
        return sorted([lp, points_c[0], rp],reverse=lower)
    
    random.shuffle(points_c)
    
    # this should be done in linear time
    lines = [ sorted(points_c[2*i:2*i+2])  for i in xrange(0,len(points_c)/2)]
    
    slopes = []
    ind = 0
    for l in lines:
        slope = (l[1][1]-l[0][1])/(l[1][0]*1.0-l[0][0])
        slopes.append((slope,ind))
        ind += 1
    sslopes = sorted(slopes)
    print sslopes
    median = sslopes[len(sslopes)/2]
    
    pmax = max(points_c + [lp,rp], key=lambda x: x[1] - median[0] * x[0])
    
    points_left = []
    points_right = []
    ind = 0
    for p in points_c:
        if not lower:
            if p[0] < pmax[0]:
                if ind%2 == 1 and slopes[ind/2]<=median:
                    pass
                else:
                    points_left.append(p)
            elif p[0] > pmax[0]:
                if ind%2 == 0 and ind!=(len(points_c)-1) and slopes[ind/2]>=median:
                    pass
                else:
                    points_right.append(p)
        else:
            if p[0] < pmax[0]:
                if ind%2 == 1 and slopes[ind/2]>=median:
                    pass
                else:
                    points_left.append(p)
            elif p[0] > pmax[0]:
                if ind%2 == 0 and ind!=(len(points_c)-1) and slopes[ind/2]<=median:
                    pass
                else:
                    points_right.append(p)
            
        ind += 1
    
    if pmax == lp:
        return DivideHull2D(points_right, lp, rp, lower)
    elif pmax == rp:
        return DivideHull2D(points_left, lp, rp, lower)
    else:
        return DivideHull2D(points_left, lp, pmax, lower) + DivideHull2D(points_right, pmax, rp, lower)




if __name__ == '__main__':
    
    points = list(set([(random.randint(50,750),random.randint(50,750)) for i in range(0,1000)])) #get rid of duplicities
    
    # i want unique values of x 
    points.sort()
    points2 = [points[0]]
    for i in points:
        if i[0] == points2[-1][0]:
            continue
        points2.append(i)
    points = points2
    
    
    random.shuffle(points)
    
    lpi = min(xrange(len(points)), key=lambda x:points[x])
    lp = points[lpi]
    points.pop(lpi)
    
    rpi = max(xrange(len(points)), key=lambda x:points[x])
    rp = points[rpi]
    points.pop(rpi)
    print points
    
    
    upper_hull = DivideHull2D(points, lp, rp, lower=False)
    
    
    print lp, rp
    print upper_hull
    
    
    