from math import pi , acos , sin , cos
from heapq import heapify,heappush,heappop
import time
import tkinter as tk
import sys


WIDTH = 1000
HEIGHT = 1000
root = tk.Tk() #creates the frame

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#89d3fa')
canvas.pack(expand=True) 

# map_na = tk.PhotoImage(file="map-of-north-america-max.gif")

# map_na.zoom(WIDTH//map_na.width(),HEIGHT//map_na.height())
# canvas.create_image(0,0,image=map_na,anchor=tk.NW)
# draw north america

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
    new_x = new_x * (WIDTH)/(x_bounds[1]-x_bounds[0]) * 0.8
    new_x += 0.1 * WIDTH

    new_y = y - y_bounds[0]
    new_y = new_y * (HEIGHT)/ (y_bounds[1]-y_bounds[0]) *0.7
    new_y = HEIGHT - new_y - 0.3 * HEIGHT

    return new_x,new_y

# edge: node1 : [(dist,node2, connection on graph)]
def add_edge(dictionary,node1,node2,dist, point1, point2,c):
    line = c.create_line(point1,point2)
    if node1 in dictionary:
        dictionary[node1].append((dist,node2,line))

    else:
        dictionary[node1] = [(dist,node2,line)]


coords = []
xnacoords = []
ynacoords = []
with open("north_america_boundaries.txt") as f_na:
    lines = f_na.readlines()
    coord_set = []
    for line in lines:
        if line != "\n":
            line = line.split()
            y = float(line[0])
            x = float(line[1])
            xnacoords.append(x)
            ynacoords.append(y)
            coord_set.append((y,x))
        else:
            coords.append(coord_set)
            coord_set = []

naxbounds = find_bounds(xnacoords)
naybounds = find_bounds(ynacoords)

for i in range(len(coords)):
    for j in range(len(coords[i])):
        coords[i][j] = convert(coords[i][j],naxbounds,naybounds)


for c in coords:
    canvas.create_polygon(c,fill="#c5f0a8")

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

def dijkstra(start,end,child_dict,canv,r):
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
                if child not in closed:
                    new_path = prev_nodes.copy()
                    new_path.append(child)
                    heappush(fringe,(dist_c + dist,child,new_path))
                    canv.itemconfig(seg,fill="red")
        counter += 1
        if counter%100 == 0:
            r.update()

    return None

def heuristic(start,end,node_d):
    if start == end:
        return 0
    else:
        return calcd(node_d[start][0],node_d[end][0])
def a_star(start,end,child_dict,nodes,canv,r):
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
                if child not in closed:
                    depth_c = dist + depth
                    fc = depth_c + heuristic(child,end,nodes)
                    path = prev.copy()
                    path.append(child)
                    heappush(fringe,(fc,depth_c,child,path))
                    canv.itemconfig(line,fill="blue")
        counter += 1
        if counter%10 == 0:
            r.update()
    return None
            

# print("Hello")
# val = a_star(city2id["Albuquerque"],city2id["Atlanta"],edges,node_dict)
# print(val)
# print(dijkstra(city2id["Albuquerque"],city2id["Atlanta"],edges))

start_city = "Albuquerque"
end_city = "Atlanta"

print("Time to create data structure",time2build," seconds")
start2 = time.perf_counter()
dijkstra_res,stations = dijkstra(city2id[start_city],city2id[end_city],edges,canvas,root)
root.update()
end2 = time.perf_counter()

points = [node_dict[s][1] for s in stations]
canvas.create_line(points,fill="green")
root.update()

start3 = time.perf_counter()
a_star_res,path_a = a_star(city2id[start_city],city2id[end_city],edges,node_dict,canvas,root)
points_a = [node_dict[sta][1] for sta in path_a]
canvas.create_line(points_a,fill="purple")
end3 = time.perf_counter()

print(start_city," to ",end_city, "with Dijkstra: ",dijkstra_res," in ", (end2-start2), " seconds.")


root.mainloop()