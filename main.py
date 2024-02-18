import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from whatsapp_api_client_python import API

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get_settings')
def get_settings():
    idInstance = request.args.get('idInstance')
    apiTokenInstance = request.args.get('apiTokenInstance')
    apiUrl = f"https://api.green-api.com/waInstance{idInstance}/getSettings/{apiTokenInstance}"

    response = requests.get(apiUrl)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch settings', 'status_code': response.status_code, 'body': response.text}), response.status_code

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    idInstance = data.get('idInstance')
    apiToken = data.get('apiToken')
    phone_number = data.get('phone')
    message_text = data.get('message')

    if not idInstance or not apiToken or not phone_number or not message_text:
        return jsonify({'error': 'Missing data'}), 400

    greenAPI = API.GreenAPI(idInstance, apiToken)
    response = greenAPI.sending.sendMessage(phone_number, message_text)
    if response.code == 200:
        return jsonify(response.data), 200
    else:
        return jsonify({'error': 'Response from API was not successful', 'code': response.code}), response.code

@app.route('/state_instance')
def state_instance():
    idInstance = request.args.get('idInstance')
    apiTokenInstance = request.args.get('apiTokenInstance')
    apiUrl = f"https://api.green-api.com/waInstance{idInstance}/getStateInstance/{apiTokenInstance}"

    response = requests.get(apiUrl)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch instance state', 'status_code': response.status_code, 'body': response.text}), response.status_code

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/send_file_by_url', methods=['POST'])
def send_file_by_url():
    data = request.json
    id_instance = data['idInstance']
    api_token = data['apiTokenInstance']
    phone_number = data['phone']
    file_url = data['fileUrl']

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'phone': phone_number + '@c.us',
        'body': file_url
    }

    response = requests.post(f'https://api.green-api.com/waInstance{id_instance}/sendFileByUrl', headers=headers, json=payload)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Error sending file', 'status_code': response.status_code}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
