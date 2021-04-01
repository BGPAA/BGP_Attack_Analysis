import igraph as ig

#g = ig.Graph(edges=[[0, 1], [2, 3]])
g = ig.Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6), (6,7)])
g.vs["label"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
g.vs["name"] = g.vs["label"]
g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
g.vs["label"].append('toto')
print(g.vs["label"])
print(g.vs(label_eq="Frank")[0].index)
print(g.vs["name"])
print(g.degree("Frank"))
layout = g.layout("kk")
g.save("graph_test.GraphML", format="graphml")
ig.plot(g,"graphCurrent.png",layout=layout)
