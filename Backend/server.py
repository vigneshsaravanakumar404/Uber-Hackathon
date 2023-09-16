from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        # Handle GET request
        param = request.args.get('param', None)  # Get 'param' from the query string
        return jsonify({"message": f"You sent the parameter: {param}"})
    
    elif request.method == 'POST':
        # Handle POST request
        data = request.json  # Get JSON data from the request body
        return jsonify({"message": f"You sent the data: {data}"})

if __name__ == '__main__':
    app.run(debug=True)