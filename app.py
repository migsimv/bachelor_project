from flask import Flask
from views import views
import sys

app = Flask(__name__,  static_url_path='/static')
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    sys.stdout.reconfigure(line_buffering=True)  

    app.debug = True  
    
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, app, use_reloader=True)
