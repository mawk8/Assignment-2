from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# тут храним все пришедшие пакеты пока сервер работает
packets = []

# принимаем пакеты от script.py, парсим и кладем в список
@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data: {data}")

    for row in data:
        # берем только то что нужно фронтенду — координаты, время, suspicious и страну
        packets.append({
            "ip":         row.get("ip address"),
            "lat":        row["Latitude"],
            "lon":        row["Longitude"],
            "timestamp":  row["Timestamp"],
            "suspicious": row["suspicious"],
            "country":    row.get("country", "??"),
        })
    return jsonify({'status': 'success'}), 200

# фронтенд забирает все накопленные пакеты через этот эндпоинт
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(packets)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
