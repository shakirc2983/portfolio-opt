from flask import Flask, jsonify, request
from flask_cors import CORS

from portfolio_opt import monte_carlo_simulation
app = Flask(__name__)

CORS(app)

@app.route("/mcs", methods=['GET'])
def mcs():
    return jsonify({"mcs": ["Test1", "Test2", "Test3"]})


@app.route("/run-mcs", methods=['POST'])
def run_mcs():
    data = request.get_json()
    simulations, tickers, start_date, end_date = data
    simulations = int(simulations)
    tickers = [item.strip() for item in tickers.split(",")]
    print(tickers)
    mcs = monte_carlo_simulation.MonteCarloSimulation(simulations, tickers, start_date, end_date)
    print(mcs)
    return jsonify('Done', 201)
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
