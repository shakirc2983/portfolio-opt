from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/mcs")
def mcs():
    return jsonify({"mcs": ["Test1", "Test2", "Test3"]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
