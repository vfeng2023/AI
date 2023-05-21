from math import pi , acos , sin , cos
from heapq import heapify,heappush,heappop
import time
import sys

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


def add_edge(dictionary,node1,node2,dist):
    if node1 in dictionary:
        dictionary[node1].append((dist,node2))

    else:
        dictionary[node1] = [(dist,node2)]
# read nodes
start = time.perf_counter()
with open("rrNodes.txt") as f:
    node_dict = dict()
    for line in f.readlines():
        id,y,x = line.split()
        y = float(y)
        x = float(x)
        node_dict[id] = (y,x)

# build graph
with open("rrEdges.txt") as f2:
    edges = dict()
    for line in f2.readlines():
        node1,node2 = line.split()
        distance = calcd(node_dict[node1],node_dict[node2])
        add_edge(edges,node1,node2,distance)
        add_edge(edges,node2,node1,distance)

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

def dijkstra(start,end,child_dict):
    closed = set()
    fringe = list()
    heapify(fringe)
    start_depth = 0
    heappush(fringe,(start_depth,start))
    while len(fringe) > 0:
        dist,id = heappop(fringe)

        if id == end:
            return dist

        if id not in closed:
            closed.add(id)
            children = child_dict[id]
            for c in children:
                dist_c,child = c
                if child not in closed:
                    heappush(fringe,(dist_c + dist,child))

    return None

def heuristic(start,end,node_d):
    if start == end:
        return 0
    else:
        return calcd(node_d[start],node_d[end])
def a_star(start,end,child_dict,nodes):
    closed = set()
    start_depth = 0
    f_start = heuristic(start,end,nodes)
    fringe = list()
    heapify(fringe)
    heappush(fringe,(f_start,start_depth,start))
    while len(fringe) > 0:
        f,depth,id = heappop(fringe)
        if id == end:
            return depth
        if id not in closed:
            closed.add(id)
            children = child_dict[id]
            for c in children:
                dist, child = c
                if child not in closed:
                    depth_c = dist + depth
                    fc = depth_c + heuristic(child,end,nodes)
                    heappush(fringe,(fc,depth_c,child))
    return None
            

# print("Hello")
# val = a_star(city2id["Albuquerque"],city2id["Atlanta"],edges,node_dict)
# print(val)
# print(dijkstra(city2id["Albuquerque"],city2id["Atlanta"],edges))

start_city = sys.argv[1]
end_city = sys.argv[2]

print("Time to create data structure",time2build)
start2 = time.perf_counter()
dijkstra_res = dijkstra(city2id[start_city],city2id[end_city],edges)
end2 = time.perf_counter()

start3 = time.perf_counter()
a_star_res = a_star(city2id[start_city],city2id[end_city],edges,node_dict)
end3 = time.perf_counter()

print(start_city," to ",end_city, "with Dijkstra: ",dijkstra_res," in ", (end2-start2), " seconds.")
print(start_city," to ",end_city, "with A*: ",a_star_res," in ", (end3-start3), " seconds.")
