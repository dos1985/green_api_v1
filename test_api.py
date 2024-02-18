import requests

idInstance = "7103906616"
apiTokenInstance  = "c1c097ab86034c1fbd3bb0264a842053982947fbb463461881"

# Формируем URL запроса
url = f"https://api.green-api.com/waInstance{idInstance}/getStateInstance/{apiTokenInstance}"

# Выполнение GET запроса без необходимости в 'payload' или 'headers' для этого API вызова
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    # Декодирование и печать ответа от API
    print(response.text)
else:
    print(f"Ошибка при получении состояния инстанса: {response.status_code}")
    # Выводим тело ответа для анализа ошибки
    print(response.text)