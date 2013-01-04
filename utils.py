COLORS = ("white", "black", "red", "green", "blue", "cyan", "yellow", "magenta")

REDBAD = "red"
GREENGOOD = "green"
BLUEDUNNO = "blue"
OUTLINE = "white"
CURRPOINT = "yellow"
UPHULL = "cyan"
LOHULL = "black"
PROCESSEDPOINT = "magenta"

CYAN = "cyan"
MAG = "magenta"
YELLOW = "yellow"
WHITE = "white"
BLACK = "black"
BROWN = "brown"
ORANGE = "orange"

import random, time,array


def partition(inarr, l, r, pivot):
    while l <= r:
        if inarr[l] <= pivot:
            l += 1
        else:
            tmp = inarr[l]
            inarr[l] = inarr[r]
            inarr[r] = tmp
            r -= 1
    return l-1

    
def get_kth(inarr, k):
    l = 0
    r = len(inarr)-1
    arr = inarr[:]
    
    while l < r:
        pivot = arr[random.randint(l,r)]
        mid = partition(arr,l,r,pivot)
        #print pivot, k, l, r, mid, arr[l:r+1]
        if k <= mid:
            r = mid
            while arr[r] == pivot and k!=r:
                r -= 1
            if k == r and arr[r] == pivot:
                return pivot
        else:
            l = mid+1
    return arr[l]
    

def show(hull, point):
    from Tkinter import Tk, Canvas
    hlavni = Tk()
    w = Canvas(hlavni, width=800, height=800)
    w.pack()
    
    
    
    hullpargs = reduce(lambda x, y: x + list(y), hull, [])
    for i in range(1, len(hullpargs), 2):
        hullpargs[i] = 800 - hullpargs[i] 

    w.create_polygon(*hullpargs, fill='', width=1, outline='red')
    
    w.create_oval(point[0], point[1], point[0], point[1], width=1)
    
    for i in range(0, 800, 50):
        w.create_oval(i, 40, i, 40, width=1)
    
    hlavni.mainloop()
    
def draw_points(canvas, points, color, **kwargs):    
    drawed = []
    for p in points:
        drawed.append(draw_point(canvas, p, color, **kwargs))
    return drawed

def draw_point(c, point, color, **kwargs):
    x, y = point
    size = kwargs.get('width', 1)
    return c.create_oval(x - 1 - size, y - 1 - size, x + 2 + size, y + 2 + size, outline=color, **kwargs)

def draw_way_of_points(canvas, points, color, **kwargs):
    kwargs['width'] = kwargs.get('width', 2)
    
    drawed = []
    for i in range(0, len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        drawed.append(canvas.create_line(x1, y1, x2, y2, fill=color, **kwargs))
    return drawed

def draw_polygon(canvas, points, color, **kwargs):
    kwargs['width'] = kwargs.get('width', 2)
    
    if len(points) > 2:
        hullpargs = reduce(lambda x, y: x + list(y), points, [])
        kwargs['fill'] = kwargs.get('fill', '')
        return canvas.create_polygon(*hullpargs, outline=color, **kwargs)
    elif len(points) == 2:
        return draw_way_of_points(canvas, points, color, **kwargs)
    elif len(points) == 1:
        return draw_point(canvas, points[0], color, **kwargs)

def draw_queue_step(c, queue, draweddict):
    while True:
        curr = queue.pop(0)
        print curr
        if curr == 'step':
            if queue[0] == 'step':
                continue
            return

        try:
            additional = curr[4]
            #print 'additional', additional
        except IndexError:
            additional = {}
        if curr[0] == 'remove':
            todel = draweddict[curr[1]]
            if type(todel) == list:
                for i in todel:
                    c.delete(i)
            else:
                c.delete(todel)
            del draweddict[curr[1]]
        #drawing        
        elif curr[0] == 'hull':
            draweddict[curr[1]] = draw_polygon(c, curr[3], curr[2], **additional)
        elif curr[0] == 'point':
            draweddict[curr[1]] = draw_point(c, curr[3], curr[2], **additional)
        elif curr[0] == 'points':
            draweddict[curr[1]] = draw_points(c, curr[3], curr[2], **additional)
        elif curr[0] == 'point_line':
            draweddict[curr[1]] = draw_way_of_points(c, curr[3], curr[2], **additional)
        elif curr[0] == 'text':
            draweddict[curr[1]] = c.create_text(curr[4][0], curr[4][1], text=curr[3])
            
if __name__ == '__main__':
    testarrs = []
    random.seed(0)
    for i in range(5):
        testarrs.append([random.randint(0,1000000) for i in range(10000000)])
    
    my1 = []
    my2 = []
    my3 = []
    t1 = time.time()
    random.seed(0)
    for i in testarrs:
        m_i = len(i)/2
        my1.append(get_kth(i, m_i))
    t2 = time.time()
    random.seed(0)
    for i in testarrs:
        m_i = len(i)/2
        my2.append(sorted(i)[m_i])
    t3 = time.time()
    random.seed(0)
    for i in testarrs:
        m_i = len(i)/2
        my3.append(get_kth(i, m_i))
    t4 = time.time()
    
    for i in range(len(testarrs)):
        if my1[i] != my2[i] or my1[i] != my3[i] :
            print i, my1[i], my2[i], my3[i]
            raise ValueError
    
    
    print t2-t1
    print t3-t2
    print t4-t3

        
        
            
    
