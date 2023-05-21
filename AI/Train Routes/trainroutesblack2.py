from math import pi , acos , sin , cos
from heapq import heapify,heappush,heappop
import time
import tkinter as tk
import sys

root = tk.Tk() #creates the frame

HEIGHT = 800
WIDTH = 800

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#89d3fa')

# canvas.pack(expand=True) 
canvas.grid(row=1,column=0)
def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R


def find_bounds(arr):
    return min(arr),max(arr)

def convert(node,x_bounds, y_bounds):
    y,x = node
    new_x = x - x_bounds[0]
    new_x = new_x * (WIDTH)/(x_bounds[1]-x_bounds[0]) * 1.0
    new_x += 0

    new_y = y - y_bounds[0]
    new_y = new_y * (HEIGHT)/ (y_bounds[1]-y_bounds[0]) *0.6
    new_y = HEIGHT - new_y - 0.3*HEIGHT

    return new_x,new_y

# edge: node1 : [(dist,node2, connection on graph)]
def add_edge(dictionary,node1,node2,dist, point1, point2,c):
    line = c.create_line(point1,point2)
    if node1 in dictionary:
        dictionary[node1].append((dist,node2,line))

    else:
        dictionary[node1] = [(dist,node2,line)]

# map_na = tk.PhotoImage(file="map-of-north-america-max.gif")

# map_na.zoom(WIDTH//map_na.width(),HEIGHT//map_na.height())
# canvas.create_image(0,0,image=map_na,anchor=tk.NW)

# read nodes
start = time.perf_counter()
y_coords = []
x_coords = []
with open("rrNodes.txt") as f:
    node_dict = dict()
    for line in f.readlines():
        id,y,x = line.split()
        y = float(y)
        x = float(x)
        node_dict[id] = [(y,x)]

        y_coords.append(y)
        x_coords.append(x)

x_range = find_bounds(x_coords)
y_range = find_bounds(y_coords)
# build graph
with open("rrEdges.txt") as f2:
    edges = dict()
    for line in f2.readlines():
        node1,node2 = line.split()
        distance = calcd(node_dict[node1][0],node_dict[node2][0])
        point1 = convert(node_dict[node1][0],x_range,y_range)
        point2 = convert(node_dict[node2][0],x_range,y_range)
        node_dict[node1].append(point1)
        node_dict[node2].append(point2)
        # node dict is now node: (lat,long), (x_canvas,y_canvas)
        add_edge(edges,node1,node2,distance,point1,point2,canvas)
        add_edge(edges,node2,node1,distance,point1,point2,canvas)

end = time.perf_counter()

time2build = end - start

# get city names
with open("rrNodeCity.txt") as f3:
    city2id = dict()
    for line in f3.readlines():
        data = line.split()
        id = data[0]
        city = " ".join(data[1:])
        city2id[city] = id
def reset(edge_dict,todel):
    for edge in edge_dict:
        connections = edge_dict[edge]
        for c in connections:
            canvas.itemconfig(c[2],fill="black")
    while len(todel) > 0:
        id = todel.pop()
        canvas.delete(id)
    canvas.update()
def dijkstra(start,end,child_dict,canv,r,speed):
    counter = 0
    closed = set()
    fringe = list()
    heapify(fringe)
    start_depth = 0
    prev_nodes = [start]
    heappush(fringe,(start_depth,start,prev_nodes))
    while len(fringe) > 0:
        dist,id,prev_nodes = heappop(fringe)

        if id == end:
            r.update()
            return dist,prev_nodes

        if id not in closed:
            closed.add(id)
            children = child_dict[id]
            for c in children:
                dist_c,child,seg = c
                canv.itemconfig(seg,fill="pink")
                if child not in closed:
                    new_path = prev_nodes.copy()
                    new_path.append(child)
                    heappush(fringe,(dist_c + dist,child,new_path))
                if child in closed:
                    canv.itemconfig(line,fill="gold")
                    
        counter += 1
        if counter>=speed:
            r.update()
            counter = 0

    return None

def heuristic(start,end,node_d):
    if start == end:
        return 0
    else:
        return calcd(node_d[start][0],node_d[end][0])
def a_star(start,end,child_dict,nodes,canv,r,speed):
    counter = 0
    closed = set()
    start_depth = 0
    f_start = heuristic(start,end,nodes)
    fringe = list()
    heapify(fringe)
    prev_nodes = [start]
    heappush(fringe,(f_start,start_depth,start,prev_nodes))
    while len(fringe) > 0:
        f,depth,id,prev = heappop(fringe)
        if id == end:
            r.update()
            return depth,prev
        if id not in closed:
            closed.add(id)
            children = child_dict[id]
            for c in children:
                dist, child,line = c
                canv.itemconfig(line,fill="blue")
                
                if child not in closed:
                    depth_c = dist + depth
                    fc = depth_c + heuristic(child,end,nodes)
                    path = prev.copy()
                    path.append(child)
                    heappush(fringe,(fc,depth_c,child,path))
                if child in closed:
                    canv.itemconfig(line,fill="gold")
                    
                    
        counter += 1
        if counter >= speed:
            counter = 0
            r.update()
    return None
def DFS(start,end,child_dict,canv,r,speed):
    counter = 0
    closed = set()
    fringe = list()

    start_depth = 0
    prev_nodes = [start]
    fringe.append((start_depth,start,prev_nodes))
    while len(fringe) > 0:
        dist,id,prev_nodes = fringe.pop()

        if id == end:
            r.update()
            return dist,prev_nodes

        if id not in closed:
            closed.add(id)
            children = child_dict[id]
            for c in children:
                dist_c,child,seg = c
                canv.itemconfig(seg,fill="purple")
                if child not in closed:
                    new_path = prev_nodes.copy()
                    new_path.append(child)
                    fringe.append((dist_c + dist,child,new_path))
                if child in closed:
                    canv.itemconfig(line,fill="gold")
                    
        counter += 1
        if counter >= speed:
            r.update()
            counter = 0

    return None
# print("Hello")
# val = a_star(city2id["Albuquerque"],city2id["Atlanta"],edges,node_dict)
# print(val)
# print(dijkstra(city2id["Albuquerque"],city2id["Atlanta"],edges))

# l1 = tk.Label(root,text="Start city:")
# l1.pack(side=tk.BOTTOM)
# input1 = tk.Entry(root,width = 20)
# input1.pack(side=tk.BOTTOM)

# l2 = tk.Label(root,text="Start city:")
# l2.pack(side=tk.BOTTOM)
# input2 = tk.Entry(root,width = 20)
# input2.pack(side = tk.BOTTOM)


# canvas.create_image(0,0,image=map_na)
# draw north america

frame = tk.Frame(root)
frame.grid(row=0,column=0)
# create buttons and stuff
startCitylabel = tk.Label(frame,text="Start city")
startCitylabel.grid(row=0,column=0)
endCitylabel = tk.Label(frame,text="End City")
endCitylabel.grid(row=1,column=0)

startCityValue = tk.Entry(frame,width=20)
endCityValue = tk.Entry(frame,width=20)
startCityValue.grid(row=0,column=1)
endCityValue.grid(row=1,column=1)

choice = tk.IntVar()
djkchoice = tk.Radiobutton(frame,text="Dijkstra",variable=choice,value=0)
astarchoice = tk.Radiobutton(frame,text="A star",variable=choice,value=1)
dfschoice = tk.Radiobutton(frame,variable=choice,value=2,text="Depth first search(uninformed)")
djkchoice.grid(row=2,column=0)
astarchoice.grid(row=3,column=0)
dfschoice.grid(row=4,column=0)

scaleLabel = tk.Label(frame,text="Speed(slow→fast)")
scaleLabel.grid(row=5,column=0)
slider = tk.Scale(frame,from_=1,to=250,orient=tk.HORIZONTAL)
slider.grid(row=5,column=1)

solutionslines = []
def run_anim():
    reset(edges,solutionslines)
    start_city = startCityValue.get()
    end_city = endCityValue.get()
    speed = slider.get()
    print("Time to create data structure",time2build," seconds")
    option = choice.get()
    if option == 0:
        dijkstra_res,stations = dijkstra(city2id[start_city],city2id[end_city],edges,canvas,root,speed)
        root.update()
        points = [node_dict[s][1] for s in stations]
        solutionslines.append(canvas.create_line(points,fill="green"))
        canvas.update()

    
    elif option == 1:
        a_star_res,path_a = a_star(city2id[start_city],city2id[end_city],edges,node_dict,canvas,root,speed)
        points_a = [node_dict[sta][1] for sta in path_a]
        newline = canvas.create_line(points_a,fill="green")
        solutionslines.append(newline)
    else:
        DFS_res,stations = DFS(city2id[start_city],city2id[end_city],edges,canvas,root,speed)
        root.update()
        points = [node_dict[s][1] for s in stations]
        solutionslines.append(canvas.create_line(points,fill="green"))
        canvas.update()
gobutton = tk.Button(frame,text="Go!",command=run_anim)
gobutton.grid(row=6,column=0)

root.mainloop()