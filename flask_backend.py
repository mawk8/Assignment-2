from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global list to store all received packets while the server is running
packets = []

# Receive and parse incoming packet data from the sender script.
@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data: {data}")

    for row in data:
        # Extract only the fields required by the frontend
        packets.append({
            "ip":         row.get("ip address"),
            "lat":        row["Latitude"],
            "lon":        row["Longitude"],
            "timestamp":  row["Timestamp"],
            "suspicious": row["suspicious"],
            "country":    row.get("country", "??"),
        })
    return jsonify({'status': 'success'}), 200

# Endpoint for the frontend to retrieve all accumulated packets.
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(packets)

# Serve the main frontend HTML file.
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
