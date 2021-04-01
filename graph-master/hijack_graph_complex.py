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
    print("annonce -> as_path",data["announce"]["as_path"])


# Get the main path of edges
def raw_to_graph_data(data):
    # Build the edges list
    as_hj = data["announce"]["asn"]
    return (as_hj)

def hj_walker(json_file):

    # Opening JSON file 
    jfile = open(json_file,'r')

    c = -1
    all_vertices = []
    # Walk through the jsons, json by json
    for j in jfile:
        c+=1
        # returns JSON object as 
        # a dictionary, 
        # don't forget to remove the trailling '\n'
        data = json.loads(j[:-1])
        #show_json_data(data)
        if data["type"] == "U" :
            vertices = raw_to_graph_data(data)
            # Deletes all doublons
            if vertices not in all_vertices:
                all_vertices.append(vertices)
    g = ig.Graph()
    vertice_number = len(all_vertices)
    g.add_vertices(vertice_number)
    g.vs["name"] = all_vertices
    g.vs["label"] = g.vs["name"]
    visual_style = {}
    visual_style["bbox"] = (2560, 1920)
    visual_style["vertex_label_dist"] = 2
    visual_style["margin"] = 50
    layout = g.layout(layout='lgl')
    g.save("output/hijack.GraphML", format="graphml")
    ig.plot(g, "output/graph.png", layout=layout, **visual_style)

    # Closing file 
    jfile.close()
    #print(partition[0])

hj_walker(sys.argv[1])
