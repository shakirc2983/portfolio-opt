from flask import Flask, jsonify
from flask_cors import cross_origin

app = Flask(__name__)

@app.route("/mcs", methods=['GET'])
@cross_origin()
def mcs():
    return jsonify({"mcs": ["Test1", "Test2", "Test3"]})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
