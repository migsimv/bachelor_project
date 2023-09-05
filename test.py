import helpers
import networkx as nx
n = 5000    
# m = [100, 500, 1000, 5000, 10000, 15000]
m = [5000]
mwei = [0.5, 2,5,10, 20,50]
for weig in mwei:
    for y in m:
        print("weight:", weig)
        for i in range(10):
            k=2
            actorGraph = []
            core = []
            bipartite = helpers.create_bipartite_graph([50] * n, [weig] * y,0.1)
            actorGraph = helpers.findConnectedActors(n,bipartite)
            core = helpers.getCore(actorGraph, k)
                  
            graph = nx.Graph()
            graph.add_nodes_from(core)
            for vertex, neigbors in core.items():
                for neighbor in neigbors:
                    graph.add_edge(vertex, neighbor)
            print(i+1, "->", len(core))
            largest_component_size = []
            components = list(nx.connected_components(graph))
            if components:
                largest_component_size = max(len(component) for component in components)

            print("largest component:", largest_component_size)
