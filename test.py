import helpers
import views
import random 
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from datetime import datetime  # Importing datetime module
import os 

n = [100, 1000, 5000, 10000] #aktoriai
m = [100, 1000, 5000, 10000] #atributai


def svoriu_histograma(arr, subtitle, size):
    interval_size = size / 10
    intervals = np.arange(0, size, interval_size)
    
    x = np.arange(0, size, interval_size)
    plt.xticks(x)
    plt.yticks([])  


    counts, edges, bars = plt.hist(arr, intervals, edgecolor='k')
    plt.bar_label(bars)
    plt.suptitle(subtitle)
    plt.xlabel('Viršūnės svoris')
    plt.ylabel('Viršūnių skaičius')

    # new code to save
    results_dir = os.path.join(os.getcwd(), 'results')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(results_dir, f'histogram_{timestamp}.png')

    plt.savefig(filename)
       
    plt.show()
    plt.close()   


def generate_hist(arr, subtitle, size):
    interval_size = size / 9  # Calculate interval size for 9 intervals (10 including the extra one)
    intervals = np.arange(0, size + interval_size, interval_size)  # Adjust range to include one more interval
    
    x = np.around(np.arange(0, size + interval_size, interval_size)).astype(int)  # Round and convert to integer
    plt.xticks(x)
    plt.yticks([])  

    counts, edges, bars = plt.hist(arr, intervals, edgecolor='k')
    plt.bar_label(bars)
    plt.suptitle(subtitle)
    plt.xlabel('Viršūnės laipsnis')
    plt.ylabel('Viršūnių skaičius')

 
    results_dir = os.path.join(os.getcwd(), 'results')

    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = os.path.join(results_dir, f'histogram_{timestamp}.png')

    # Save the histogram to the results directory
    plt.savefig(filename)
    # plt.show()

    plt.close()  # Close the figure after saving


def calculate_average_closure_coefficient(local_closure_coefficients, vertices):
    if local_closure_coefficients:
        return round (sum(local_closure_coefficients.values()) / vertices, 5)
    else:
        return 0
        
def calculate_weights(xm, alpha, length):
    res = []
    # random.seed(14)
    for vertice in range(length):
        weight = xm / (pow(random.random(), 1/alpha))
        res.append(weight)
    return res
        
def calculate_degrees(graph):
    degrees = [len(neighbors) for neighbors in graph.values()]
    return degrees


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
    
rez_og_clust = []
rez_og_closure = []
rez_og_tankis = []
rez_core_clust = []
rez_core_closure = []
rez_core_tankis = []

for aktorius in n:
    print("aktoriu skaicius:", aktorius)
    for atributas in m:
        print("atributu skaicius:", atributas)
        for i in range(5):
            k=2
            actorGraph = []
            core = []
            aktoriu_svoriai = []
            atributu_svoriai = []
            print("TEST: ", i)

            aktoriu_svoriai = calculate_weights(2, 4, aktorius)
            atributu_svoriai = calculate_weights(4, 6, atributas)
            # print(max(aktoriu_svoriai))
            # print(max(atributu_svoriai))
            bipartite = helpers.create_bipartite_graph(aktoriu_svoriai, atributu_svoriai, 0.1)
            actorGraph = helpers.findConnectedActors(aktorius, bipartite)

            #grafo skaiciavimai
            coefs_og = views.get_coefs(actorGraph)
            avg_clust_og = calculate_average_closure_coefficient(coefs_og[0], len(actorGraph))
            avg_closure_og = calculate_average_closure_coefficient(coefs_og[1], len(actorGraph))
            tankis_og = calculate_tankis(actorGraph)

            #serdies skaiciavimai
            core = helpers.getCore(actorGraph, k)
            coefs = views.get_coefs(core)
            avg_clust_serdis = calculate_average_closure_coefficient(coefs[0], len(core))
            avg_closure_serdis = calculate_average_closure_coefficient(coefs[1], len(core))
            tankis_serdis = calculate_tankis(core)
            rez_og_clust.append(avg_clust_og)
            rez_og_closure.append(avg_closure_og)
            rez_og_tankis.append(tankis_og)
            rez_core_clust.append(avg_clust_serdis)
            rez_core_closure.append(avg_closure_serdis)
            rez_core_tankis.append(tankis_serdis)

            print("og ir serdies dydis: ", len(actorGraph), len(core))
            print("og ir serdies  Clustering: ", avg_clust_og, avg_clust_serdis)
            print("og ir serdies Closure: ", avg_closure_og, avg_closure_serdis)
            print("og ir serdies TANKIS: ", tankis_og, tankis_serdis)
            # if i == 1:
            # aktoriu `svoriu histograma
            svoriu_histograma(aktoriu_svoriai, 'Aktorių viršūnių svoriai', 10)

            # atributu svoriu histograma
            svoriu_histograma(atributu_svoriai, 'Atributų viršūnių svoriai', 10)

            # grafo laipsniu histograma
            max_neighbors = 0
            max_vertex = None

            for vertex, neighbors in actorGraph.items():
                num_neighbors = len(neighbors)
                if num_neighbors > max_neighbors:
                    max_neighbors = num_neighbors
                    max_vertex = vertex
            print(max_neighbors)
            rounded_max_neighbors = ((max_neighbors + 9) // 10) * 10  # Round to the nearest ten

            arr = calculate_degrees(actorGraph)
            print(rounded_max_neighbors)
            generate_hist(arr, 'Grafo viršūnių laipsniai, viršūnių skaičius =  {}'.format(len(actorGraph)), rounded_max_neighbors)
            max_neighbors1 = 0
            max_vertex1 = None

            for vertex1, neighbors1 in core.items():
                num_neighbors1 = len(neighbors1)
                if num_neighbors1 > max_neighbors1:
                    max_neighbors1 = num_neighbors1
                    max_vertex1 = vertex1
            print(max_neighbors1)
            rounded_max_neighbors1 = ((max_neighbors1 + 9) // 10) * 10  # Round to the nearest ten

            # serdies laipsniu histograma
            arr = calculate_degrees(core)
            print(rounded_max_neighbors)
            generate_hist(arr, 'Aktorių šerdies viršūnių laipsniai, viršūnių skaičius =  {}'.format(len(core)), rounded_max_neighbors1)

            
print("og clust:")
for o in rez_og_clust:
    print(o)
print("og closure:")
for o in rez_og_closure:
    print(o)
print("og tankis:")
for o in rez_og_tankis:
    print(o)

print("core clust:")
for o in rez_core_clust:
    print(o)
print("core closure:")
for o in rez_core_closure:
    print(o)
print("core tankis:")
for o in rez_core_tankis:
    print(o)