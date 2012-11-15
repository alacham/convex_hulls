'''
Created on 13.11.2012

@author: jirka
'''


def vector_multip_determ(p1, p2, point):
    diag1 = (p2[0] - p1[0]) * (point[1] - p1[1])
    diag2 = (p2[1] - p1[1]) * (point[0] - p1[0])
    return diag1 - diag2

def is_3rd_left(p1,p2,p3):
    if vector_multip_determ(p1, p2, p3) < 0:
        return True
    return False



def graham_scan(points):
    hulls = ([],[])
    iters = (iter(points),reversed(points))
    for hull, piter in zip(hulls, iters):
        for i in piter:
            if len(hull) <= 1:
                hull.append(i)
            else:
                while len(points) > 1 and not is_3rd_left(hull[-2], i, hull[-1]):
                    hull.pop()
                hull.append(i)
    return hulls[1] + hulls[0][1:-1]
    



class ChanHull(object):
    '''
    classdocs
    '''


    def __init__(self,params):
        '''
        Constructor
        '''
        