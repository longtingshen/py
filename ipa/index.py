from flask import Flask

app = Flask(__name__)

@app.route('/', methods=["GET"])
def return_OneText():
    return "fina_res"
