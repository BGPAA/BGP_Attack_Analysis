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
    print("as_path",data["as_path"])

# Get the main path of edges
def raw_to_graph_data(data):
    # Build the edges list
    edges=[]
    as_path = data["as_path"]
    nexts_edges_u = as_path.split(" ")
    #print("nexts_edges_u",nexts_edges_u)
    # Convert raw data to int list
    nexts_edges = []
    for i in nexts_edges_u:
        nexts_edges.append(int(i))
    #print("nexts_edges",nexts_edges)
    # Convert the list to couples of int
    for i in range(len(nexts_edges) - 1):
        edges.append([nexts_edges[i], nexts_edges[i+1]])
    #print("edges",edges)
    vertices = nexts_edges
    #print("vertices",vertices)
    return (edges,vertices)

def set_hijacks(data):
    hijacks = data["announce"]["asn"]
    return hijacks

def route_walker(json_file_route, json_file_hijack):

    # Opening JSON file
    asn_hijacked = []
    with open(json_file_hijack, "r") as file:
        for line in file:
            data = json.loads(line[:-1])
            if data["type"] == "U":
                hj = set_hijacks(data)
                if hj not in asn_hijacked:
                    asn_hijacked.append(hj)

    jfile = open(json_file_route,'r')

    c = -1
    weights = []
    hijacks = []
    all_edges = []
    all_vertices = []
    # Walk through the jsons, json by json
    for j in jfile:
        c+=1
        #print('\nLINE ' + str(c)) 
        #print('json',j)
        # returns JSON object as 
        # a dictionary, 
        # don't forget to remove the trailling '\n'
        data = json.loads(j[:-1])
        #show_json_data(data)
        if data["action"] == "A":
            if '{' in data["as_path"]:
                data["as_path"] = data["as_path"].replace("{","").replace("}","").replace(","," ")
            (edges,vertices) = raw_to_graph_data(data)
            # Deletes all doublons
            for i in edges : 
                if i not in all_edges:
                    #print("i",i)
                    all_edges.append(i)
                    weights.append(1)
                else:
                    weights[all_edges.index(i)] += 1
            for i in vertices :
                if i not in all_vertices:
                    all_vertices.append(i)
                    if i in asn_hijacked:
                        hijacks.append(True)
                    else:
                        hijacks.append(False)
    #print("all_edges",all_edges)
    #print("all_vertices",all_vertices)
    #print(all_edges)
    g = ig.Graph()
    vertice_number = len(all_vertices)
    #print("vertice_number",vertice_number)
    g.add_vertices(vertice_number)
    g.vs["name"] = all_vertices
    g.vs["label"] = g.vs["name"]
    g.es["weight"] = weights
    g.vs["hijack"] = hijacks
    #print("len weight", len(weights))
    #print("len edges", len(all_edges))
    #print(weights)
    #print("labels",g.vs["label"])
    #print("174",all_vertices.index(174))
    #print("174",g.vs(label_eq=174)[0].index)
    for i in all_edges:
        #print("edge",i)
        #print("labels",g.vs(label_eq=i[0])[0].index,g.vs(label_eq=i[1])[0].index)
        g.add_edges([ (g.vs(label_eq=i[0])[0].index, g.vs(label_eq=i[1])[0].index) ])
    #print(g)
    g.es["weight"] = weights
    #print("g.es weight", g.es["weight"])
    g.save("output/routes.graphML", format="graphml")
    print("connexe ? : " + str(g.is_connected()))

    # Closing file 
    jfile.close()
    #print(partition[0])

route_walker(sys.argv[1], sys.argv[2])
