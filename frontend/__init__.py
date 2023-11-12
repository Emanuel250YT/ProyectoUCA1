from flask import Flask
from . import mainRoutes

app = Flask(__name__)


mainRoutes.setMainRoutes(app)


def startFrontend():
    app.run(port=80, debug=True)
