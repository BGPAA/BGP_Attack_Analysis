# Python program to read 
# json file 

import json 
import igraph as ig

# Opening JSON file 
f = open('samples/n1.hijacks.json',) 

# returns JSON object as 
# a dictionary 
data = json.load(f) 

# Iterating through the json 
# list 
print(data)
print("asn",data["asn"])
print("peer_as",data["peer_as"])
print("as_path",data["announce"]["as_path"])

# Build the edges list
edges=[]

# Get the main path of edges
as_path = data["announce"]["as_path"]
nexts_edges_u = as_path.split(" ")
print("nexts_edges_u",nexts_edges_u)
# Convert raw data to int list
nexts_edges = []
for i in nexts_edges_u:
    nexts_edges.append(int(i))
print("nexts_edges",nexts_edges)
# Convert the list to couples of int
for i in range(len(nexts_edges) - 1):
    edges.append([nexts_edges[i], nexts_edges[i+1]])
print("edges",edges)
# Adds the last edge
last_edge = [nexts_edges[-2],data["asn"]]
print("last_edge",last_edge)
edges.append(last_edge)
print("edges",edges)

# Instantiate the Graph
g = ig.Graph()

# Add the right number of vertices
vertice_number = len(nexts_edges)+1
print("vertice_number",vertice_number)
g.add_vertices(vertice_number)

# Add the edges
for i in range(vertice_number - 2):
    g.add_edge(i,i+1)
g.add_edge(vertice_number-3,vertice_number-1)
edges.append((vertice_number-3,vertice_number-1))
print("edges",edges)
print(g)

# Assign the labels to the vertices
g.vs["label"]= nexts_edges + [data["asn"]]
# Choose a layout
layout = g.layout(layout='circle')
# Display the graph
ig.plot(g, layout=layout)

# Closing file 
f.close() 

