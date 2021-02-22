from flask import Flask
from flask_restful import Api

from resource.ocr import ocr

app = Flask(__name__)
api = Api(app)

api.add_resource(ocr, "/ocr/")

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port='8000')