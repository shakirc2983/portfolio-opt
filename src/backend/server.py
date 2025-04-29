from flask import Flask, jsonify, request
from flask_cors import CORS

from portfolio_opt import monte_carlo_simulation as MCS
app = Flask(__name__)

CORS(app)

@app.route("/mcs", methods=['GET'])
def mcs():
    return jsonify({"mcs": ["Test1", "Test2", "Test3"]})


@app.route("/run-mcs", methods=['POST'])
def run_mcs():
    data = request.get_json()
    print(data)
    return jsonify('Done', 201)
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
