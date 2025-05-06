from flask import Flask, jsonify, request
from flask_cors import CORS
from pypfopt import expected_returns, risk_models, objective_functions
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt import black_litterman
from pypfopt.efficient_frontier import EfficientFrontier
from portfolio_opt import monte_carlo_simulation

import traceback
import yfinance as yf
import pandas as pd
import numpy as np


app = Flask(__name__)

CORS(app)

simulation_result = None


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


@app.route("/portfolio/<int:portfolio_id>")
def portfolio(portfolio_id):
    if "simulation_result" not in globals():
        return jsonify({"error": "No simulation data available"}), 400

    try:
        portfolio = simulation_result.get_portfolio(portfolio_id)
        if not portfolio or not hasattr(portfolio, "weights"):
            return jsonify({"error": "Invalid portfolio ID"}), 404

        print("Has it gone through?")
        return (
            jsonify(
                {
                    "tickers": getattr(simulation_result, "tickers", []),
                    "weights": portfolio.weights.tolist(),
                    "returns": portfolio.expected_returns,
                    "volatility": portfolio.expected_volatility,
                }
            ),
            201,
        )

    except ValueError:
        print("ValueError")
        return jsonify({"error": "Portfolio ID must be an integer"}), 400

    except Exception as e:
        print("Exception: ", e)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/run-bl", methods=["POST"])
def bl():
    data = request.get_json()
    # Extract input data
    tickers = [item.strip() for item in data["tickers"].split(",")]
    start_date = data["start_date"]
    end_date = data["end_date"]
    views = data.get("views", {})
    confidences = data.get("confidences", {})

    try:

        prices = yf.download(tickers, start=start_date, end=end_date)["Close"]

        if isinstance(prices, pd.Series):
            prices = pd.DataFrame(prices)
            prices.columns = [tickers[0]]

        prices.dropna(inplace=True)

        if prices.shape[0] < 2:
            return (
                jsonify(
                    {
                        "error": "Insufficient data for analysis. Please select a wider date range."
                    }
                ),
                400,
            )

        mu = expected_returns.mean_historical_return(prices)
        S = risk_models.sample_cov(prices)

        risk_aversion = 1.0

        market_caps = pd.Series(
            [1] * len(prices.columns),
            index=prices.columns,
        )

        bl_params = {
            "cov_matrix": S,
            "pi": "market",
            "risk_aversion": risk_aversion,
            "market_caps": market_caps,
        }

        valid_views = {}
        valid_confidence_list = []

        for ticker, view_return in views.items():
            if ticker in prices.columns:
                valid_views[ticker] = view_return
                valid_confidence_list.append(confidences.get(ticker, 0.5))

        if valid_views:

            bl_params["absolute_views"] = valid_views
            bl_params["omega"] = "idzorek"
            bl_params["view_confidences"] = np.array(valid_confidence_list)

        bl = BlackLittermanModel(**bl_params)

        posterior_returns = bl.bl_returns()
        posterior_cov = bl.bl_cov()

        ef = EfficientFrontier(posterior_returns, posterior_cov)
        ef.add_objective(objective_functions.L2_reg, gamma=0.1)

        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        performance = ef.portfolio_performance(verbose=False)

        formatted_weights = {
            ticker: round(weight, 4) for ticker, weight in cleaned_weights.items()
        }

        print("\n=== Black-Litterman Optimization Results ===")
        print("Weights:")
        for ticker, weight in formatted_weights.items():
            print(f"  {ticker}: {weight}")
        print(f"Expected Return: {round(performance[0], 4)}")
        print(f"Volatility:      {round(performance[1], 4)}")
        print(f"Sharpe Ratio:    {round(performance[2], 4)}")
        print("============================================\n")

        return (
            jsonify(
                {
                    "data": {
                        "weights": formatted_weights,
                        "expected_return": round(performance[0], 4),
                        "volatility": round(performance[1], 4),
                        "sharpe_ratio": round(performance[2], 4),
                    }
                }
            ),
            201,
        )
    except Exception as e:
        import traceback

        error_trace = traceback.format_exc()
        print(f"Error in Black-Litterman optimization: {str(e)}\n{error_trace}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
