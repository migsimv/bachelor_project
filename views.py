from flask import Blueprint, url_for,redirect,render_template, request, jsonify, make_response
import helpers
from flask import Flask, request
from werkzeug.utils import secure_filename

views = Blueprint(__name__,'views')

@views.route('/upload_file', methods=['POST'])
def upload_file_route():
    file = request.files['fileUpl']
    print("AAAA")
    if file:
        file.save('uploads/' + file.filename)
        return 'File uploaded successfully', 200
    else:
        return 'No file uploaded', 400
    
def get_result_file(file, k):
    print(file, k)
    return 0

@views.route('/', methods=['GET', 'POST'])
def index():
    files = helpers.get_files_in_uploads_folder()
    if request.method == 'POST':
            if request.form.get('selected_file'):
                decoded_lines = helpers.read_selected_file_content(request.form.get('selected_file'))
            else:
                decoded_lines = []
                file = request.files['fileUpl']
                lines = file.readlines()  
                for line in lines:
                    decoded_line = line.decode('utf-8')  
                    decoded_lines.append(decoded_line.strip()) 
            b = request.form['digit']
            # print(file)
            # get_result_file(a,b)
            graph = {}
            for line in decoded_lines:
              parts = line.split('->')
              node = int(parts[0])
              neighbors = list(map(int, parts[1].split()))
              graph[node] = neighbors
            print(graph)
            # core = helpers.getCore(graph, b)
            # res = helpers.getResult(core)
            # komp = helpers.find_components(core)
            # ilg = komp[0]

            # for array in komp:
            #     ilg = [len(array) for array in komp]

            # komp = helpers.find_components(core)
            # virsunes = len(core)
            # plot_data_before = generate_plot(core, 'test5')
            # plot_data_core = generate_plot(graph, 'test')
            plot_data_before = 0
            plot_data_core =0
            return render_template('res.html',virsunes=[])

            # return render_template('res.html',virsunes=virsunes,plot_data_before = plot_data_core, plot_data = plot_data_before, selected_content =a, selected_content2 =res, modified_content=b, komponentes = len(komp), ilgiausia = len(ilg))
    return render_template('index.html', files = files)

