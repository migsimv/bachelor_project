from flask import Blueprint, url_for,redirect,render_template, request, jsonify
import os
views = Blueprint(__name__,'views')


# Helper function to get a list of files in the "uploads" folder
def get_files_in_uploads_folder():
    uploads_folder = "uploads"  # Folder name where the files are stored
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
    
    # Save the new text file in the "uploads" folder
    save_new_file(filename, content)
    
    return jsonify({"success": True})

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                file.save(os.path.join("uploads", file.filename))
                # with open(os.path.join("uploads", file.filename), 'r') as f:
                #     num_lines = len(f.readlines())
                    
                # return f'Text file "{file.filename}" uploaded successfully. Number of lines: {num_lines}'

        elif 'selected_file' in request.form:
            selected_file = request.form['selected_file']
            selected_content = read_selected_file_content(selected_file)
            files_in_uploads = get_files_in_uploads_folder()

            # return render_template('index.html', files=files_in_uploads, selected_content=selected_content)

    # Get the list of files in the "uploads" folder
    files_in_uploads = get_files_in_uploads_folder()
    return render_template('index.html', files=files_in_uploads)

@views.route('/testing', methods=['GET'])
def testing():
    print("AAAA")
    return render_template('res.html')

@views.route('/run_testing_function', methods=['GET'])
def run_testing_function():

    return redirect(url_for('views.testing'))