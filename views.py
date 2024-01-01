from flask import Blueprint, render_template, request
import helpers
import matplotlib
matplotlib.use('Agg') 
from matplotlib import pyplot as plt
import time
import numpy as np
import threading
import networkx as nx
plot_lock = threading.Lock()
views = Blueprint(__name__,'views')

last_generated_plots = []  

@views.route('/upload_file', methods=['POST'])
def upload_file_route():
    file = request.files['fileUpl']
    if file:
        file.save('uploads/' + file.filename)
        return 'File uploaded successfully', 200
    else:
        return 'No file uploaded', 400

def get_result_from_adj_list(graph, k):
    data = {}
    graphComponents = helpers.find_components(graph)
    data["graphComponents"] =len( graphComponents)
    data["graphVertices"] = len(graph)
    data["maxGraphComponent"] = helpers.longest_inner_array_length(graphComponents)
    graphnx = nx.Graph()
    graphnx.add_nodes_from(graph)
    for vertex, neigbors in graph.items():
        for neighbor in neigbors:
            graphnx.add_edge(vertex, neighbor)
    core2= nx.k_core(graphnx, int(k))
    data["core"] = nx.to_dict_of_lists(core2)

    # data["core"] = helpers.getCore(graph, k)
    data["coreToPrint"] = helpers.getResult(data["core"])
    data["coreVertices"] = len(data["core"])
    coreComponents = helpers.find_components(data["core"])
    data["coreComponents"] = len(coreComponents)
    data["maxCoreComponent"] = helpers.longest_inner_array_length(coreComponents)

    return data


@views.route('/', methods=['GET', 'POST'])
def index():
    files = helpers.get_files_in_uploads_folder()
    santykis = 0
    if request.method == 'POST':
            if request.form['options'] == 'option1': #getting graph
                if request.form.get('selected_file'):
                    decoded_lines = helpers.read_selected_file_content(request.form.get('selected_file'))
                else:
                    decoded_lines = []
                    file = request.files['fileUpl']
                    lines = file.readlines()  
                    for line in lines:
                        decoded_line = line.decode('utf-8')  
                        decoded_lines.append(decoded_line.strip()) 
                graph = helpers.getGraph(decoded_lines)
            elif request.form['options'] == 'option2':
                xLen =  int(request.form.get('xLen'))
                xWeight =  int(request.form.get('xWeight'))
                yLen =  int(request.form.get('yLen'))
                yWeight =  int(request.form.get('yWeight'))
                alpha = float(request.form.get('alpha'))
                xArray = [xWeight for _ in range(xLen)]
                yArray = [yWeight for _ in range(yLen)]
                bipartiteGraph = helpers.create_bipartite_graph(xArray, yArray, alpha)
                graph = helpers.findConnectedActors(xLen, bipartiteGraph) #actorsGraph
                santykis = round((xWeight/yWeight), 4)
            else:
                xArray = [int(value.strip()) for value in (request.form.get('xArray')).split(",")]
                yArray = [int(value.strip()) for value in (request.form.get('yArray')).split(",")]
                alpha = float(request.form.get('alpha2'))
                bipartiteGraph = helpers.create_bipartite_graph(xArray, yArray, alpha)
                graph = helpers.findConnectedActors(len(xArray), bipartiteGraph) #actorsGraph
            #working with the graph
            k = request.form['digit']
            data = get_result_from_adj_list(graph, k)
            if santykis != 0:
                data['santykis'] = santykis
            data['k'] = k
            data['originalGraph'] =  helpers.getResult(graph)
            print((data['originalGraph']))
            print(graph)
            degreesArray = []
            for key, value in graph.items():
                degreesArray.append(len(value))
            coreDegreesArray = []
            for key, value in data["core"].items():
                coreDegreesArray.append(len(value))
            data['plot_filename1'] = generate_plot(degreesArray, 'Aktorių grafo viršūnių laipsniai')
            data['plot_filename2'] = generate_plot(coreDegreesArray, 'Šerdies viršūnių laipsniai')
            closure_coef_checked = request.form.get('closureCoef') == 'on'

            if closure_coef_checked:
                graph_cof = get_coefs(graph)
                cor_cof = get_coefs(data["core"])
                data['clust_coef_org'] = graph_cof[0]
                data['clust_coef_cor'] = cor_cof[0]
                data['average_clust_org'] = helpers.calculate_average_closure_coefficient( data['clust_coef_org'])
                data['average_clust_cor'] = helpers.calculate_average_closure_coefficient( data['clust_coef_cor'])

                data['closure_coef_org'] = graph_cof[1]
                data['closure_coef_cor'] = cor_cof[1]
                data['average_closure_org'] = helpers.calculate_average_closure_coefficient( data['closure_coef_org'])
                data['average_closure_cor'] = helpers.calculate_average_closure_coefficient( data['closure_coef_cor'])

            return render_template('res.html', files=files, data=data)
    return render_template('index.html', files = files)

def get_coefs(graph):
    G = nx.Graph()
    G.add_nodes_from(graph.keys())
    for source, targets in graph.items():
        for target in targets:
            G.add_edge(source, target)

    clustering = {}
    closure = {}
    for node in G.nodes():
        clustering_coefficient = helpers.calculate_local_clustering_coefficient(G, node)
        closure_coefficient =  helpers.calculate_local_closure_coefficient(G, node)
        clustering[node] = clustering_coefficient
        closure[node] = closure_coefficient
    return [clustering, closure]

def generate_plot(arr, subtitle):
    with plot_lock:
        intervals = []
        for i in range(0, 30, 3):
            intervals.append(i)
        # intervals.append(1000 - 1)

        x = np.arange(0, 30, 3)
        y = np.arange(0, 5000, 200)
        plt.xticks(x)
        plt.yticks(y)

        counts, edges, bars = plt.hist(arr, intervals, edgecolor='k')
        plt.bar_label(bars)
        plt.suptitle(subtitle)
        plt.xlabel('Viršūnės laipsnis')
        plt.ylabel('Viršūnių skaičius')

        timestamp = int(time.time())
        if (subtitle == 'Šerdies viršūnių laipsniai' ):
            filename='histogram_{timestamp}aaa.jpg'
            plot_filename = f'static/{filename}'
        else:
            filename='histogram_{timestamp}.jpg'
            plot_filename = f'static/{filename}'

        plt.savefig(plot_filename, format='jpeg', dpi=300)
        plt.close()
    
        return filename