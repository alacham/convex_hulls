'''
Created on 12.10.2012

@author: jirka
'''
import math


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


def recurrent_qhull(lm, rm, plist, is_upper=True):
    if not plist:
        return []
    line = (lm, rm)
    most_distant = max(plist, key=lambda x: geoPointLineDist(x, line, testSegmentEnds=False))
    lhull = set()
    rhull = set()
    for pi in plist:
        if is_3_out(lm, most_distant, pi, is_upper):
            lhull.add(pi)
        elif is_3_out(most_distant, rm, pi, is_upper):
            rhull.add(pi)
    
    return recurrent_qhull(lm, most_distant, lhull, is_upper) + [most_distant] +\
        recurrent_qhull(most_distant, rm, rhull, is_upper)

    


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





def quick_hull(points):
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
    
    hull = [lmost] + recurrent_qhull(lmost, rmost, uhull, is_upper= True) +\
        [rmost] + list(reversed(recurrent_qhull(lmost, rmost, dhull, is_upper= False)))
    return hull

        
        
if __name__ == '__main__':
    from Tkinter import Tk, Canvas
    hlavni = Tk()
    w = Canvas(hlavni, width=800, height=800)
    w.pack()
    pointlist = set([(417, 355), (713, 712), (318, 170), (437, 453), (470, 188), (527, 133), (636, 376), (191, 572), (230, 488), (707, 288), (347, 188), (250, 317), (486, 170), (624, 189), (592, 306), (341, 489), (480, 208), (352, 439), (293, 385), (687, 337), (99, 367), (415, 669), (321, 630), (131, 269), (722, 527), (102, 226), (723, 256), (326, 76), (226, 219), (195, 187), (522, 610), (249, 682), (701, 263), (75, 356), (138, 400), (554, 92), (624, 744), (55, 341), (296, 637), (616, 370), (532, 744), (350, 228), (74, 221), (733, 453), (161, 84), (577, 738), (575, 445), (468, 662), (69, 523), (679, 492), (195, 545), (518, 127), (600, 239), (451, 624), (323, 244), (95, 77), (138, 180), (112, 488), (544, 642), (357, 132), (311, 101), (190, 175), (451, 365), (466, 526), (320, 295), (278, 210), (553, 260), (146, 722), (211, 692), (580, 253), (690, 694), (206, 270), (194, 567), (376, 608), (533, 402), (445, 324), (376, 383), (120, 564), (322, 455), (548, 394), (335, 109), (584, 470), (362, 211), (709, 468), (610, 150), (150, 392), (406, 290), (583, 329), (544, 92), (206, 204), (488, 478), (293, 350), (179, 201), (196, 452), (477, 744), (121, 472), (121, 463), (626, 548), (666, 258), (357, 281), (682, 526), (149, 170), (743, 511), (599, 90), (536, 236), (114, 287), (710, 337), (164, 308), (53, 339), (50, 461), (295, 623), (606, 149), (646, 390), (295, 120), (218, 389), (329, 647), (173, 245), (211, 685), (529, 173), (76, 168), (625, 686), (594, 311), (428, 521), (391, 155), (228, 184), (527, 676), (618, 396), (175, 198), (454, 642), (711, 274), (522, 156), (542, 589), (178, 106), (207, 396), (589, 390), (640, 352), (526, 409), (606, 587), (221, 65), (613, 571), (466, 543), (148, 558), (185, 284), (436, 646), (465, 636), (97, 237), (260, 78), (76, 371), (640, 498), (293, 270), (521, 397), (376, 632), (95, 280), (438, 520), (654, 245), (148, 453), (326, 167), (293, 572), (613, 201), (102, 201), (194, 614), (73, 166), (59, 306), (331, 553), (393, 54), (213, 669), (720, 119), (150, 82), (199, 566), (542, 606), (659, 683), (337, 683), (272, 684), (667, 663), (212, 748), (102, 486), (536, 209), (67, 215), (334, 633), (154, 566), (570, 674), (592, 176), (620, 286), (261, 59), (680, 324), (83, 509), (373, 52), (439, 522), (267, 124), (167, 222), (152, 111), (320, 450), (119, 167), (675, 361), (590, 303), (195, 563), (74, 640), (503, 226), (325, 588), (499, 382)])
    for point in pointlist:
        w.create_oval(point[0],point[1],point[0],point[1],width=1)
    qh = quick_hull(pointlist)
    print qh
    
    hullpargs = reduce(lambda x,y: x + list(y), qh.points(), [])
    
    w.create_polygon(*hullpargs,fill='',width=1,outline='red')
    
    
    hlavni.mainloop()
