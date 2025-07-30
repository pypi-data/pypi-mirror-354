import threading
import webbrowser
from flask import Flask, request, render_template_string
from .downloader import download_media

app = Flask(__name__)

with open(__file__.replace("webapp.py", "static/index.html")) as f:
    HTML_TEMPLATE = f.read()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_ = request.form['format']
    quality = request.form['quality']
    result = download_media(url, format_, quality)
    return f"<pre>{result}</pre>"

def start_server():
    threading.Thread(target=lambda: app.run(port=8000)).start()
    webbrowser.open("http://localhost:8000")
