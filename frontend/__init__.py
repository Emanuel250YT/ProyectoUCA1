from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def startFrontend():
    app.run(port=80, debug=True)
