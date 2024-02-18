import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from whatsapp_api_client_python import API
import logging



# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  # Получаем логгер для текущего файла


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

    response = requests.get(apiUrl)  # Заголовки не требуются, так как токен передается в URL

    # Возврат ответа в зависимости от статуса запроса
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

    # Проверка наличия всех необходимых данных
    if not idInstance or not apiToken or not phone_number or not message_text:
        return jsonify({'error': 'Missing data'}), 400

    greenAPI = API.GreenAPI(idInstance, apiToken)

    try:
        response = greenAPI.sending.sendMessage(phone_number, message_text)
        if response.code == 200:
            return jsonify(response.data), 200
        else:
            return jsonify({'error': 'Ответ от API не успешен', 'code': response.code}), response.code
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        return jsonify({'error': str(e)}), 500



@app.route('/state_instance')
def state_instance():
    idInstance = request.args.get('idInstance')
    apiTokenInstance = request.args.get('apiTokenInstance')
    apiUrl = f"https://api.green-api.com/waInstance{idInstance}/getStateInstance/{apiTokenInstance}"

    response = requests.get(apiUrl)

    # Логируем результат запроса
    if response.status_code == 200:
        logger.info(f"Successfully fetched instance state: {response.json()}")
        return jsonify(response.json()), 200
    else:
        logger.error(f"Failed to fetch instance state, status code: {response.status_code}, response: {response.text}")
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

    response = requests.post(f'https://api.green-api.com/waInstance{id_instance}/sendFileByUrl', headers=headers,
                             json=payload)

    # Обрабатываем ответ
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Ошибка при отправке файла', 'status_code': response.status_code}), response.status_code



# Запустите сервер
if __name__ == '__main__':
    app.run(debug=True)
