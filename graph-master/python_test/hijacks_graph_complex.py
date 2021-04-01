# Python program to read 
# json file 

import json 
import igraph as ig
import sys

# Print useful data fileds
def show_json_data(data):
    print('data',data)
    print("asn",data["asn"])
    print("peer_as",data["peer_as"])
    print("as_path",data["announce"]["as_path"])

# Get the main path of edges
def raw_to_graph_data(data):
    # Build the edges list
    edges=[]
    as_path = data["announce"]["as_path"]
    nexts_edges_u = as_path.split(" ")
    #print("nexts_edges_u",nexts_edges_u)
    # Convert raw data to int list
    nexts_edges = []
    for i in nexts_edges_u:
        nexts_edges.append(int(i))
    print("nexts_edges",nexts_edges)
    # Convert the list to couples of int
    for i in range(len(nexts_edges) - 1):
        edges.append([nexts_edges[i], nexts_edges[i+1]])
    print("edges",edges)
    last_edge = [nexts_edges[-1],data["asn"]]
    print("last_edge",last_edge)
    edges.append(last_edge)
    print("edges",edges)
    vertices = nexts_edges + [data["asn"]]
    print("vertices",vertices)
    return (edges,vertices)

def hj_walker(json_file):

    # Opening JSON file 
    jfile = open(json_file,'r')

    c = -1
    # Walk through the jsons, json by json
    for j in jfile:
        c+=1
        print('\nLINE ' + str(c)) 
        print('json',j)
        # returns JSON object as 
        # a dictionary, 
        # don't forget to remove the trailling '\n'
        data = json.loads(j[:-1])
        show_json_data(data)
        raw_to_graph_data(data)
    

    # Closing file 
    jfile.close() 

hj_walker(sys.argv[1])
