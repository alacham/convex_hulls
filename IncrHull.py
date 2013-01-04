'''
Created on 30.9.2012

@author: J. Machala, 324543
'''

import bintrees.rbtree as rbtree
import random, sys
from utils import *
from symbol import except_clause


def vector_multip_determ(p1, p2, point):
    diag1 = (p2[0] - p1[0]) * (point[1] - p1[1])
    diag2 = (p2[1] - p1[1]) * (point[0] - p1[0])
    return diag1 - diag2


def is_3_out(p_list, is_upper=True):
    if p_list[0] < p_list[1]:
        determ = vector_multip_determ(p_list[0], p_list[1], p_list[2])
    else:
        determ = vector_multip_determ(p_list[1], p_list[0], p_list[2])
    if (is_upper and determ > 0) or (not is_upper and determ < 0):
        return True
    return False

def is_2_out(p_list, is_upper=True):
    if p_list[0] < p_list[1]:
        determ = vector_multip_determ(p_list[0], p_list[2], p_list[1])
    else:
        determ = vector_multip_determ(p_list[1], p_list[2], p_list[0])
    if (is_upper and determ > 0) or (not is_upper and determ < 0):
        return True
    return False


class IncrHull(object):
    
    def __init__(self):
        self.pointSet = set()
        self.upperRBT = rbtree.RBTree()
        self.bottomRBT = rbtree.RBTree()
        self.leftmost = None
        self.rightmost = None
        self.pointCounter = 0
        self.drawQueue = []
        
    def points(self):
        if self.pointCounter == 0:
            return []
        elif self.pointCounter == 1:
            return [self.leftmost]
        p_list = []
        for i in self.upperRBT.keys():
            p_list.append(i)
        p_list.pop()
        for i in self.bottomRBT.keys(reverse=True):
            p_list.append(i)
        p_list.pop()
        return p_list
        
    
    def add_point(self, point):
        dellater = []
        if point in self.pointSet:
            return False
        self.pointSet.add(point)
        self.pointCounter += 1
        
        if self.pointCounter > 1:
            self.drawQueue.append(('hull', 'hull', OUTLINE, self.points(),dict(width=2,dash=(4,7))))
            dellater.append('hull')
            self.drawQueue.append(('step'))
        self.drawQueue.append(('point', 'p'+str(point), CURRPOINT, point,dict(width=3)))
        self.drawQueue.append(('step'))

        if self.pointCounter == 1:
            self.leftmost = point
            self.rightmost = point
            self.upperRBT[point] = 1
            self.bottomRBT[point] = 1
        # 2. bod
        elif self.pointCounter == 2:
            if point < self.leftmost:
                self.leftmost = point
            else:
                self.rightmost = point
            self.upperRBT[point] = 1
            self.bottomRBT[point] = 1
        # 3. a dalsi bod
        # je to maximum nebo minimum
        elif point < self.leftmost or point > self.rightmost:
            if point > self.rightmost:
                self.rightmost = point
                reverser = True
            else:
                self.leftmost = point
                reverser = False
            self.upperRBT[point] = 1
            self.bottomRBT[point] = 1
            trees = (self.upperRBT, self.bottomRBT)
            is_hull_upper = (True, False)
            # pripadne mazat z obou...
            self.drawQueue.append(('point_line', 'hull'+str(True), UPHULL, list(trees[0].keys()),dict(width=3,dash=(5,5),dashoffset=3)))
            self.drawQueue.append(('point_line', 'hull'+str(False), LOHULL, list(trees[1].keys()),dict(width=3,dash=(5,5))))
            self.drawQueue.append(('step'))
            for tree, is_upper in zip(trees, is_hull_upper):
                dellist = []
                curr_points = []
                for p in tree.keys(reverser):
                    curr_points.append(p)
                    if len(curr_points) == 3:
                        self.drawQueue.append(('point_line', 'curpoints', BLUEDUNNO, curr_points[:]))
                        self.drawQueue.append(('step'))
                        if is_2_out(curr_points, is_upper):
                            self.drawQueue.append(('remove', 'curpoints'))
                            self.drawQueue.append(('point_line', 'curpoints', GREENGOOD, curr_points[:]))
                            self.drawQueue.append(('step'))
                            self.drawQueue.append(('remove', 'curpoints'))
                            break
                        self.drawQueue.append(('remove', 'curpoints'))
                        self.drawQueue.append(('point_line', 'curpoints', REDBAD, curr_points[:]))
                        dellist.append(curr_points.pop(1))
                        self.drawQueue.append(('point', 'd'+str(dellist[-1]), REDBAD, dellist[-1],dict(width=4)))
                        self.drawQueue.append(('step'))
                        self.drawQueue.append(('remove', 'curpoints'))
                self.drawQueue.append(('remove', 'hull'+str(is_upper)))
                for key in dellist:
                    self.drawQueue.append(('remove', 'd'+str(key)))
                    del tree[key]
                self.drawQueue.append(('point_line', 'hull'+str(is_upper), CURRPOINT, list(tree.keys()),dict(width=2)))
                self.drawQueue.append(('step'))
                dellater.append('hull'+str(is_upper))
        # hledat ve stromech atd
        else:
            skip = False
            determ = vector_multip_determ(self.leftmost, self.rightmost, point)
            # horni/dolni obal
            if determ > 0:
                tree = self.upperRBT
                upper = True
            elif determ < 0:
                tree = self.bottomRBT
                upper = False
            else:
                skip = True
            
            if not skip:
                self.drawQueue.append(('hull', 'onetree', LOHULL, list(tree.keys()),dict(width=2,dash=(5,5),dashoffset=2)))
                self.drawQueue.append(('step'))
                prev = tree.keyslice(startkey=point, endkey=None, reverse=True)
                succ = tree.keyslice(startkey=point, endkey=None, reverse=False)
                p_prev = prev.next()
                p_succ = succ.next()
                
                self.drawQueue.append(('point', 'c'+str(p_prev), BLUEDUNNO, p_prev,dict(width=3)))
                self.drawQueue.append(('point', 'c'+str(p_succ), BLUEDUNNO, p_succ,dict(width=3)))
                self.drawQueue.append(('step'))
                
                
                if not is_3_out([p_prev, p_succ, point], upper):
                    self.drawQueue.append(('point', 'd'+str(point), REDBAD, point,dict(width=4)))
                    self.drawQueue.append(('step'))
                    self.drawQueue.append(('remove', 'c'+str(p_prev)))
                    self.drawQueue.append(('remove', 'c'+str(p_succ)))
                    self.drawQueue.append(('remove', 'd'+str(point)))
                    dellater.append('onetree')
                    #draw some shit
                    pass
                else:
                    self.drawQueue.append(('point', 'a'+str(point), GREENGOOD, point,dict(width=4)))
                    self.drawQueue.append(('step'))
                    dellist = []
                    test_point_lists = ([point, p_succ], [point, p_prev])
                    iters = (succ, prev)
                    cntr = 0
                    for curr_points, iterer in zip(test_point_lists, iters):
                        cntr += 1
                        self.drawQueue.append(('remove', 'c'+str(curr_points[-1])))
                        for p in iterer:
                            curr_points.append(p)
                            self.drawQueue.append(('point_line', 'curpoints', BLUEDUNNO, curr_points[:]))
                            self.drawQueue.append(('step'))
                            if is_2_out(curr_points, upper):
                                self.drawQueue.append(('remove', 'curpoints'))
                                self.drawQueue.append(('point_line', 'curpoints', GREENGOOD, curr_points[:]))
                                self.drawQueue.append(('step'))
                                self.drawQueue.append(('remove', 'curpoints'))
                                break
                            else:
                                self.drawQueue.append(('remove', 'curpoints'))
                                self.drawQueue.append(('point_line', 'curpoints', REDBAD, curr_points[:]))
                                dellist.append(curr_points.pop(1))
                                self.drawQueue.append(('point', 'd'+str(dellist[-1]), REDBAD, dellist[-1],dict(width=4)))
                                self.drawQueue.append(('step'))
                                self.drawQueue.append(('remove', 'curpoints'))
                        self.drawQueue.append(('point_line', 'curpoints'+str(cntr), CURRPOINT, curr_points+list(iterer)))
                        self.drawQueue.append(('step'))
                    
                    for k in dellist:
                        self.drawQueue.append(('remove', 'd'+str(k)))
                        del tree[k]
                    self.drawQueue.append(('step'))
                    tree[point] = 1
                    self.drawQueue.append(('remove', 'curpoints'+str(1)))
                    self.drawQueue.append(('remove', 'curpoints'+str(2)))
                    self.drawQueue.append(('remove', 'onetree'))
                    self.drawQueue.append(('hull', 'onetree2', CURRPOINT, list(tree.keys()),dict(width=3)))
                    dellater.append('onetree2')
                    
                    self.drawQueue.append(('step'))
                    self.drawQueue.append(('remove', 'a'+str(point)))
        
        for i in dellater:
            self.drawQueue.append(('remove', i))
        self.drawQueue.append(('remove', 'p'+str(point)))
        self.drawQueue.append(('point', 'p'+str(point), PROCESSEDPOINT, point,dict(width=2)))
        

if __name__ == '__main__':
    points = []
    myhull2 = IncrHull()
    

#    for i in range(100000):
#        point = (random.randint(0,10000),random.randint(0,10000))
#        points.append(point)
#        myhull2.add_point(point)
#    print len(myhull2.points())
    
    
    from Tkinter import Tk, Canvas
    hlavni = Tk()
    
    canvas = Canvas(hlavni, width=800, height=800)
    canvas.pack()
    points = []

    
    
    initgenerator = [(random.randint(50,750),random.randint(50,750)) for i in range(100)]
    #initgenerator = [(417, 355), (713, 712), (318, 170), (437, 453), (470, 188), (527, 133), (636, 376), (191, 572), (230, 488), (707, 288), (347, 188), (250, 317), (486, 170), (624, 189), (592, 306), (341, 489), (480, 208), (352, 439), (293, 385), (687, 337), (99, 367), (415, 669), (321, 630), (131, 269), (722, 527), (102, 226), (723, 256), (326, 76), (226, 219), (195, 187), (522, 610), (249, 682), (701, 263), (75, 356), (138, 400), (554, 92), (624, 744), (55, 341), (296, 637), (616, 370), (532, 744), (350, 228), (74, 221), (733, 453), (161, 84), (577, 738), (575, 445), (468, 662), (69, 523), (679, 492), (195, 545), (518, 127), (600, 239), (451, 624), (323, 244), (95, 77), (138, 180), (112, 488), (544, 642), (357, 132), (311, 101), (190, 175), (451, 365), (466, 526), (320, 295), (278, 210), (553, 260), (146, 722), (211, 692), (580, 253), (690, 694), (206, 270), (194, 567), (376, 608), (533, 402), (445, 324), (376, 383), (120, 564), (322, 455), (548, 394), (335, 109), (584, 470), (362, 211), (709, 468), (610, 150), (150, 392), (406, 290), (583, 329), (544, 92), (206, 204), (488, 478), (293, 350), (179, 201), (196, 452), (477, 744), (121, 472), (121, 463), (626, 548), (666, 258), (357, 281), (682, 526), (149, 170), (743, 511), (599, 90), (536, 236), (114, 287), (710, 337), (164, 308), (53, 339), (50, 461), (295, 623), (606, 149), (646, 390), (295, 120), (218, 389), (329, 647), (173, 245), (211, 685), (529, 173), (76, 168), (625, 686), (594, 311), (428, 521), (391, 155), (228, 184), (527, 676), (618, 396), (175, 198), (454, 642), (711, 274), (522, 156), (542, 589), (178, 106), (207, 396), (589, 390), (640, 352), (526, 409), (606, 587), (221, 65), (613, 571), (466, 543), (148, 558), (185, 284), (436, 646), (465, 636), (97, 237), (260, 78), (76, 371), (640, 498), (293, 270), (521, 397), (376, 632), (95, 280), (438, 520), (654, 245), (148, 453), (326, 167), (293, 572), (613, 201), (102, 201), (194, 614), (73, 166), (59, 306), (331, 553), (393, 54), (213, 669), (720, 119), (150, 82), (199, 566), (542, 606), (659, 683), (337, 683), (272, 684), (667, 663), (212, 748), (102, 486), (536, 209), (67, 215), (334, 633), (154, 566), (570, 674), (592, 176), (620, 286), (261, 59), (680, 324), (83, 509), (373, 52), (439, 522), (267, 124), (167, 222), (152, 111), (320, 450), (119, 167), (675, 361), (590, 303), (195, 563), (74, 640), (503, 226), (325, 588), (499, 382)]
    tkinterpoints = {}
    
    for point in initgenerator:
        points.append(point)
        myhull2.add_point(point)
        tkinterpoints[point] = canvas.create_oval(point[0],point[1],point[0],point[1],width=1)
        
    animqueue = myhull2.drawQueue
    ddict = {}
    
    def do_something(tkintevent):
        draw_queue_step(canvas,animqueue, ddict)

    canvas.bind('<Button-1>', do_something)
    hlavni.mainloop()
    
