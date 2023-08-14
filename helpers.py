import os
import matplotlib.pyplot as plt
import base64  
import io


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
        line = "{} {} {}".format(res[0], res[1], ' '.join(str(x) for x in res[2]))
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

def generate_plot(graph, name): #BUG nucrashina po kurio laiko RuntimeError: main thread is not in main loop
    intervals = []
    for i in range(0, 1000, 100):
        intervals.append(i)
    intervals.append(1000 - 1)
    degreesArray = []
    print(graph)
    for key, value in graph.items():
        degreesArray.append(len(value))
    # x = np.arange(0, 1000, 100)
    # y = np.arange(0, 5000, 200)
    x = [1, 2, 3, 4, 5]
    y = [10, 5, 7, 2, 8]

    plt.figure(figsize=(4.5, 4))  
    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.suptitle(name)

    # plt.title('Sample Plot')
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.switch_backend('agg')

    plt.close() 
    return plot_data