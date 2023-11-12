from flask import Flask, render_template
from . import mainRoutes

app = Flask(__name__)


mainRoutes.setMainRoutes(app)


def startFrontend():
    app.run(port=80, debug=True)
