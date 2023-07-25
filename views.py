from flask import Blueprint, url_for,redirect,render_template, request, jsonify, make_response
import os
views = Blueprint(__name__,'views')

def get_files_in_uploads_folder():
    uploads_folder = "uploads"  
    files = os.listdir(uploads_folder)
    return files

def read_selected_file_content(selected_file):
    with open(os.path.join("uploads", selected_file), 'r') as f:
        content = f.read()
    return content

def save_new_file(filename, content):
    with open(os.path.join("uploads", filename), 'w') as f:
        f.write(content)
        
@views.route('/save_new_file', methods=['POST'])
def save_new_file_route():
    filename = request.form['filename']
    content = request.form['content']
    
    save_new_file(filename, content)
    
    return jsonify({"success": True})

@views.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            a = file.read()
            b = request.form['digit']
            return render_template('res.html',selected_content =a,   modified_content =b)
    return render_template('index.html')
