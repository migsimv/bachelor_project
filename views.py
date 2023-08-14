from flask import Blueprint, render_template, request
import helpers

views = Blueprint(__name__,'views')

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
            # plot_data_before = generate_plot(core, 'test5')
            # plot_data_core = generate_plot(graph, 'test')
            plot_data_before = 0
            plot_data_core =0
            # print(data['originalGraph'])
            # print(data['coreToPrint'])
            return render_template('res.html', files=files, data=data)
    return render_template('index.html', files = files)
