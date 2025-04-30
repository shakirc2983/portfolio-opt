from flask import Flask, jsonify, request
from flask_cors import CORS

from portfolio_opt import monte_carlo_simulation

app = Flask(__name__)

CORS(app)


@app.route("/mcs", methods=["GET"])
def mcs():
    return jsonify({"mcs": ["Test1", "Test2", "Test3"]})


@app.route("/run-mcs", methods=["POST"])
def run_mcs():

    data = request.get_json()
    simulations, tickers, start_date, end_date = data
    simulations = int(simulations)
    tickers = [item.strip() for item in tickers.split(",")]
    try:
        global simulation_result
        simulation_result = monte_carlo_simulation.MonteCarloSimulation(
            simulations, tickers, start_date, end_date
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    result = {
        "simulations": simulation_result.simulations,
        "min_volatility": simulation_result.min_volatility_value(),
        "max_volatility": simulation_result.max_volatility_value(),
        "max_sharpe": simulation_result.max_sharpe_value(),
        "min_sharpe": simulation_result.min_sharpe_value(),
    }
    return jsonify({"data": result}), 201


@app.route("/ef")
def ef():
    if "simulation_result" not in globals():
        return jsonify({"error": "No simulation data available"}), 400

    try:
        vol_arr, ret_arr, sharpe_arr = zip(
            *[
                (p.expected_volatility, p.expected_returns, p.sharpe_ratio)
                for p in simulation_result.portfolios
            ]
        )
        return jsonify(
            {"x": list(vol_arr), "y": list(ret_arr), "sharpe": list(sharpe_arr)}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
