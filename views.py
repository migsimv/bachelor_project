from flask import Blueprint, url_for,redirect,render_template, request, jsonify, make_response
import os
views = Blueprint(__name__,'views')

def get_files_in_uploads_folder():
    uploads_folder = "uploads"  
    files = os.listdir(uploads_folder)
    return files

def read_selected_file_content(selected_file):
    with open(os.path.join("uploads", selected_file), 'r') as f:
        content = f.readlines()
    return [line.strip() for line in content]


def save_new_file(filename, content):
    with open(os.path.join("uploads", filename), 'w') as f:
        f.write(content)
        
@views.route('/save_new_file', methods=['POST'])
def save_new_file_route():
    filename = request.form['filename']
    content = request.form['content']
    
    save_new_file(filename, content)
    
    return jsonify({"success": True})

def getVertexDegrees(graph):
    count = []
    num_vertices = len(graph)
    for vertex in range(num_vertices):
        count.append(len(graph[vertex]))
    return count

def getCore(file, k):
    graph = {}
    for line in file:
        parts = line.split('->')
        node = int(parts[0])
        neighbors = list(map(int, parts[1].split()))
        graph[node] = neighbors

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
        line = "{} {} {}".format(res[0], res[1], ' '.join(str(x) for x in res[2]))
        result.append(line)
    return result

@views.route('/', methods=['GET', 'POST'])
def index():
    files = get_files_in_uploads_folder()
    if request.method == 'POST':
            print("CCC")
            if  request.form.get('selected_file'):
                file = read_selected_file_content(request.form.get('selected_file'))
                a = file
            else:
                file = request.files['fileUpl']
                a =(file.readlines()).decode('utf-8') 
            b = request.form['digit']
            core = getCore(a, b)
            res = getResult(core)
            komp = find_components(core)

            ilg = komp[0]

            for array in komp:
                ilg = [len(array) for array in komp]

            komp = find_components(core)
            print(komp)
            return render_template('res.html', selected_content =res, selected_content2 =a, modified_content=b, komponentes = len(komp), ilgiausia = len(ilg))
    return render_template('index.html', files = files)

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
