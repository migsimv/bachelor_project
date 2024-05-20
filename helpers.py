from collections import defaultdict
import os
import matplotlib
matplotlib.use('TkAgg')
import random
import math
import sys
import networkx as nx
import itertools
sys.setrecursionlimit(5000)


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
        neighbors = list(map(int, parts[1].split(', ')))
        graph[node] = neighbors
    return graph
        
def calculate_weights(xm, alpha, length):
    res = []
    for vertice in range(length):
        weight = xm / (pow(random.random(), 1/alpha))
        res.append(weight)
    return res

def create_bipartite_graph(xArray, yArray, alpha, socModel):
    V = len(xArray) + len(yArray)

    adj_list = [[] for i in range(V)]
    if socModel == 'model1':
        for i in range(len(xArray)):
            f = 0
            for j in range(len(xArray), V):
                p = getP(alpha, xArray[i], yArray[f], len(xArray), len(yArray))
                if random.random() < p:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
                f += 1
    elif socModel == 'model2':
        adjusted_xArray = [int(x) for x in xArray]

        adjusted_yArray = [int(y) for y in yArray]
        sum_top = sum(adjusted_xArray)
        sum_bottom = sum(adjusted_yArray)
        print(sum_top)
        print(sum_bottom)
        while sum_top != sum_bottom:
            if sum_top > sum_bottom:
                index_to_remove = random.randint(0, len(adjusted_xArray) - 1)
                if adjusted_xArray[index_to_remove] > 0:
                    adjusted_xArray[index_to_remove] -= 1
                    sum_top -= 1
            else:
                index_to_remove = random.randint(0, len(adjusted_yArray) - 1)
                if adjusted_yArray[index_to_remove] > 0:
                    adjusted_yArray[index_to_remove] -= 1
                    sum_bottom -= 1
        
        top_vertices = list(range(len(adjusted_xArray)))
        bottom_vertices = list(range(len(adjusted_yArray)))
        print(sum_top)
        print(sum_bottom)
        # Create connection points
        top_connection_points = []
        bottom_connection_points = []
        
        for vertex, degree in zip(top_vertices, adjusted_xArray):
            top_connection_points.extend([vertex] * degree)
        
        for vertex, degree in zip(bottom_vertices, adjusted_yArray):
            bottom_connection_points.extend([vertex + len(adjusted_xArray)] * degree)
        
        # Shuffle connection points
        random.shuffle(top_connection_points)
        random.shuffle(bottom_connection_points)
        
        # Create adjacency list
        adj_list = defaultdict(list)
        
        for top_point, bottom_point in zip(top_connection_points, bottom_connection_points):
            adj_list[top_point].append(bottom_point)
            adj_list[bottom_point].append(top_point)
        
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

def calculate_local_clustering_coefficient(G, node): 
    neighbors = nx.neighbors(G, node)
    neighbor_pairs = list(itertools.combinations(neighbors, 2))
    closed_pairs = [pair for pair in neighbor_pairs if G.has_edge(pair[0], pair[1])]
    if len(closed_pairs) != 0:
        return  round((len(closed_pairs) / len(neighbor_pairs)), 3)
    else:
        return 0

def calculate_local_closure_coefficient(G, node): 
    triangles = nx.triangles(G, node)
    wedges =count_2_edge_paths_starting_from_node(G, node)
    if triangles == 0 or wedges == 0:
        return 0
    else:
        return round((2 * triangles / wedges), 3)


def calculate_average_closure_coefficient(local_closure_coefficients):

    if local_closure_coefficients:
        return round (sum(local_closure_coefficients.values()) / len(local_closure_coefficients), 5)
    else:
        return 0
        
def count_2_edge_paths_starting_from_node(graph, start_node):
    neighbors = list(graph.neighbors(start_node))
    sum_degrees = 0

    for neighbor in neighbors:
        sum_degrees += graph.degree(neighbor) - 1

    return sum_degrees

def calculate_tankis(graph):
    virsuniu_laipsniai = calculate_degrees(graph)
    visos_poros = len(graph) * len(graph)
    laipsniu_suma = 0
    for laipsnis in virsuniu_laipsniai:
        laipsniu_suma += laipsnis
    if laipsniu_suma:
        return round((laipsniu_suma / 2) / visos_poros, 8)
    else: 
        return 0
    
def calculate_degrees(graph):
    degrees = [len(neighbors) for neighbors in graph.values()]
    return degrees
