

def show(hull, point):
    from Tkinter import Tk, Canvas
    hlavni = Tk()
    w = Canvas(hlavni, width=800, height=800)
    w.pack()
    
    
    
    hullpargs = reduce(lambda x,y: x + list(y), hull, [])
    for i in range(1,len(hullpargs),2):
        hullpargs[i] = 800 - hullpargs[i] 

    w.create_polygon(*hullpargs,fill='',width=1,outline='red')
    
    w.create_oval(point[0],point[1],point[0],point[1],width=1)
    
    for i in range(0,800,50):
        w.create_oval(i,40,i,40,width=1)
    
    hlavni.mainloop()
    
def draw_points(canvas, points, color):
    drawed = []
    for x,y in points:
        drawed.append(canvas.create_oval(x-2,y-2,x+3,y+3,outline=color))
    return drawed

def draw_way_of_points(canvas, points, color):
    drawed = []
    for i in range(0,len(points)-1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        drawed.append(canvas.create_line(x1,y1,x2,y2,fill=color))
    return drawed

def draw_polygon(canvas, points, color, width):
    hullpargs = reduce(lambda x,y: x + list(y), points, [])
    return canvas.create_polygon(*hullpargs,fill='',width=width,outline=color)
