import bfs
from flask import Flask, render_template, jsonify
TEMPLATES_AUTO_RELOAD = True
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_path/<A>/<B>")
def get_path(A, B):
    A = A.lower()
    B = B.lower()
    return jsonify(bfs.server_runner(A, B))
    #return jsonify({
    #    "titles": [A, "something", B],
    #    "ids": [1, 2, 3]
    #    })

if __name__ == '__main__':
    app.run(debug=True)
