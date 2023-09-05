import os
import matplotlib
matplotlib.use('TkAgg')
import random
import math

def get_files_in_uploads_folder():
    uploads_folder = "uploads"  
    files = os.listdir(uploads_folder)
    return files

def read_selected_file_content(selected_file):
    with open(os.path.join("uploads", selected_file), 'r') as f:
        content = f.readlines()
    return [line.strip() for line in content]
        
def getVertexDegrees(graph):
    count = []
    num_vertices = len(graph)
    for vertex in range(num_vertices):
        count.append(len(graph[vertex]))
    return count

def getCore(graph, k):
    core = graph.copy()
    degrees = getVertexDegrees(core)
    removed = True
    while removed:
        removed = False
        for i in range(len(graph)):
            if degrees[i] < int(k) and degrees[i] > 0:
                for neighbor in core[i]:
                    core[neighbor].remove(i)
                    degrees[neighbor] -= 1
                core.pop(i)
                degrees[i] = 0
                removed = True
            elif degrees[i] == 0 and core.get(i) is not None:
                core.pop(i)
                removed = True
    return core

def getResult(graph):
    result = []
    for key, value in graph.items():
        res = (key, "->", value)
        line = "{} {} {}".format(res[0], res[1], ', '.join(str(x) for x in res[2]))
        result.append(line)
    return result

def find_components(graph):
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components


def longest_inner_array_length(array_of_arrays):
    longest_length = 0
    for inner_array in array_of_arrays:
        current_length = len(inner_array)
        if current_length > longest_length:
            longest_length = current_length
    return longest_length

def getGraph(decoded_lines):
    graph = {}
    for line in decoded_lines:
        parts = line.split('->')
        node = int(parts[0])
        neighbors = list(map(int, parts[1].split()))
        graph[node] = neighbors
    return graph

def create_bipartite_graph(xArray, yArray, alpha):
    V = len(xArray) + len(yArray)
    # random.seed(42)
    adj_list = [[] for i in range(V)]
    for i in range(len(xArray)):
        f = 0
        for j in range(len(xArray), V):
            p = getP(alpha, xArray[i], yArray[f], len(xArray), len(yArray))
            if random.random() < p:
                adj_list[i].append(j)
                adj_list[j].append(i)
            f += 1
    return adj_list

def getP(alpha,x,y,n,m):
    return alpha * (x*y) / math.sqrt(n*m)

def findConnectedActors(x, graph): 
    neighbors = {}
    new_graph = {}
    for i in range(x):
        for neighbor in graph[i]:
            neighbors.setdefault(neighbor, []).append(i)
    for i in range(x):
        new_graph[i] = list({n for neighbor in graph[i] for n in neighbors.get(neighbor, {}) if n != i})
    return new_graph