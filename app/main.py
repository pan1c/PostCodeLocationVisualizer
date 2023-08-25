from flask import Flask, render_template_string
from modules import map_generator

app = Flask(__name__)

@app.route('/')
def show_map():
    html_code = map_generator.generate_map_html()
    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
