# api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    if 'email' not in data or '@' not in data['email']:
        return jsonify({'error': 'Invalid email'}), 400

    if 'price' not in data or data['price'] > 1000:
        return jsonify({'error': 'Price must be $1000.00 or less'}), 400

    print('Received data:', data)      # prints to console where API is running
    return jsonify({'status': 'ok', 'received': data}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)