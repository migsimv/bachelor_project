from flask import Blueprint, render_template, request
import helpers
import matplotlib
matplotlib.use('Agg') 
from matplotlib import pyplot as plt
import time
import numpy as np
import threading

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
    data["core"] = helpers.getCore(graph, k)
    data["coreToPrint"] = helpers.getResult(data["core"])
    data["coreVertices"] = len(data["core"])
    coreComponents = helpers.find_components(data["core"])
    data["coreComponents"] = len(coreComponents)
    data["maxCoreComponent"] = helpers.longest_inner_array_length(coreComponents)

    return data


@views.route('/', methods=['GET', 'POST'])
def index():
    files = helpers.get_files_in_uploads_folder()
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
            else:
                xArray = [int(value.strip()) for value in (request.form.get('xArray')).split(",")]
                yArray = [int(value.strip()) for value in (request.form.get('yArray')).split(",")]
                alpha = float(request.form.get('alpha2'))
                bipartiteGraph = helpers.create_bipartite_graph(xArray, yArray, alpha)
                graph = helpers.findConnectedActors(len(xArray), bipartiteGraph) #actorsGraph
            #working with the graph
            k = request.form['digit']
            data = get_result_from_adj_list(graph, k)
            data['k'] = k
            data['originalGraph'] =  helpers.getResult(graph)

            degreesArray = []
            for key, value in graph.items():
                degreesArray.append(len(value))
            coreDegreesArray = []
            for key, value in graph.items():
                coreDegreesArray.append(len(value))
            data['plot_filename1'] = generate_plot(degreesArray, 'Aktorių grafo viršūnių laipsniai')
            data['plot_filename2'] = generate_plot(coreDegreesArray, 'Šerdies viršūnių laipsniai')
            
            return render_template('res.html', files=files, data=data)
    return render_template('index.html', files = files)

def generate_plot(arr, subtitle):
    with plot_lock:
        intervals = []
        for i in range(0, 1000, 100):
            intervals.append(i)
        intervals.append(1000 - 1)

        x = np.arange(0, 1000, 100)
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