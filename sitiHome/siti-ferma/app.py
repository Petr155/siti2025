from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
from threading import Lock
import serial
import time


# Конфигурация MQTT
BROKER = "192.168.42.1"
PORT = 1883
topics = {
    'temperature': '/devices/wb-msw-v4_11/controls/Temperature',
    'humidity': '/devices/wb-msw-v4_11/controls/Humidity',
    'CO2': '/devices/wb-msw-v4_11/controls/CO2',
    'temp_wather':'/devices/wb-adc/controls/A1',
    'ph_wather':'/devices/wb-adc/controls/A2',
    'm_wather':'/devices/wb-adc/controls/A3',
    'level_wather':'/devices/wb-adc/controls/A4',
}
# Топики для реле
MQTT_TOPIC_RELAY_1 = "/devices/wb-mr6c_137/controls/K1/on"  
MQTT_TOPIC_RELAY_2 = "/devices/wb-mr6c_137/controls/K2/on" 
MQTT_TOPIC_RELAY_3 = "/devices/wb-mr6c_137/controls/K3/on"  
MQTT_TOPIC_RELAY_4 = "/devices/wb-mr6c_137/controls/K4/on" 
MQTT_TOPIC_RELAY_5 = "/devices/wb-mr6c_137/controls/K5/on"  
MQTT_TOPIC_RELAY_6 = "/devices/wb-mr6c_137/controls/K6/on"  

# Глобальные переменные для хранения данных
data = {'temperature': 'N/A', 'humidity': 'N/A', 'CO2': 'N/A', 'temp_wather': 'N/A', 'ph_wather': 'N/A', 'm_wather': 'N/A', 'level_wather': 'N/A'}
data_lock = Lock()

# Инициализация MQTT клиента
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """Callback при подключении к MQTT-брокеру"""
    if rc == 0:
        print("Подключено к MQTT-брокеру")
        for topic in topics.values():
            client.subscribe(topic)
    else:
        print(f"Ошибка подключения: {rc}")

def on_message(client, userdata, msg):
    """Callback при получении сообщения"""
    global data
    with data_lock:
        for key, topic in topics.items():
            if msg.topic == topic:
                data[key] = msg.payload.decode()
                #print(f"Обновлено: {key} = {data[key]}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

# Функция для отправки команды на реле
def set_relay(topic, state):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.publish(topic, state)
    client.disconnect()
    

# Инициализация Flask
app = Flask(__name__)

@app.route('/')
def home():
    """Главная страница"""
    return render_template('index.html')

@app.route('/data')
def get_data():
    """Возвращает данные в формате JSON"""
    with data_lock:
        return jsonify(data)
        
# Маршруты для управления реле
@app.route('/relay1/on', methods=['POST'])
def relay1_on():
    set_relay(MQTT_TOPIC_RELAY_1, "1")
    return jsonify({"status": "success", "message": "Включено"})

@app.route('/relay1/off', methods=['POST'])
def relay1_off():
    set_relay(MQTT_TOPIC_RELAY_1, "0")
    return jsonify({"status": "success", "message": "Выключено"})

@app.route('/relay2/on', methods=['POST'])
def relay2_on():
    set_relay(MQTT_TOPIC_RELAY_2, "1")
    return jsonify({"status": "success", "message": "Включено"})

@app.route('/relay2/off', methods=['POST'])
def relay2_off():
    set_relay(MQTT_TOPIC_RELAY_2, "0")
    return jsonify({"status": "success", "message": "Выключено"})

@app.route('/relay3/on', methods=['POST'])
def relay3_on():
    set_relay(MQTT_TOPIC_RELAY_3, "1")
    return jsonify({"status": "success", "message": "Включено"})

@app.route('/relay3/off', methods=['POST'])
def relay3_off():
    set_relay(MQTT_TOPIC_RELAY_3, "0")
    return jsonify({"status": "success", "message": "Выключено"})

@app.route('/relay4/on', methods=['POST'])
def relay4_on():
    set_relay(MQTT_TOPIC_RELAY_4, "1")
    return jsonify({"status": "success", "message": "Включено"})

@app.route('/relay4/off', methods=['POST'])
def relay4_off():
    set_relay(MQTT_TOPIC_RELAY_4, "0")
    return jsonify({"status": "success", "message": "Выключено"})

@app.route('/relay5/on', methods=['POST'])
def relay5_on():
    set_relay(MQTT_TOPIC_RELAY_5, "1")
    return jsonify({"status": "success", "message": "Включено"})

@app.route('/relay5/off', methods=['POST'])
def relay5_off():
    set_relay(MQTT_TOPIC_RELAY_5, "0")
    return jsonify({"status": "success", "message": "Выключено"})

@app.route('/relay6/on', methods=['POST'])
def relay6_on():
    set_relay(MQTT_TOPIC_RELAY_6, "1")
    return jsonify({"status": "success", "message": "Включено"})

@app.route('/relay6/off', methods=['POST'])
def relay6_off():
    set_relay(MQTT_TOPIC_RELAY_6, "0")
    return jsonify({"status": "success", "message": "Выключено"})

if __name__ == '__main__':
    try:
        # Запуск Flask-сервера
        app.run(host='192.168.42.1', port=5001, debug=True)
    except KeyboardInterrupt:
        # Остановка MQTT-клиента при завершении
        mqtt_client.loop_stop()
        mqtt_client.disconnect()