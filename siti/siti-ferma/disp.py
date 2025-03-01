from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
from threading import Lock
from datetime import datetime
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

# Настройка UART для дисплея Nextion
nextion_port = "/dev/ttyUSB0"  # Порт, к которому подключен дисплей
baudrate = 9600  # Скорость передачи данных

# Функция для отправки команды на дисплей
def send_command(command):
    with serial.Serial(nextion_port, baudrate, timeout=1) as ser:
        ser.write(command.encode('utf-8'))
        ser.write(b'\xFF\xFF\xFF')  # Завершающие байты

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

# Основной цикл
while True:
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    
    #дата и время
    now = datetime.now()

    # Форматирование даты
    date = now.strftime("%d.%m.%Y")  # День.Месяц.Год
    tim = now.strftime('%H:%M:%S')
    command_date = f't14.txt="{date}"'
    command_time = f't13.txt="{tim}"'


    # Чтение данных с датчика
    tem = data['temperature']
    hum = data['humidity']
    co2 = data['CO2']

    # Формирование команды для дисплея
    command_tem = f't10.txt="{tem}"'
    command_hum = f't11.txt="{hum}"'
    command_co2 = f't12.txt="{co2}"'

    # Отправка команды на дисплей
    send_command(command_tem)
    send_command(command_hum)
    send_command(command_co2)
    send_command(command_date)
    send_command(command_time)

    # Пауза перед следующим обновлением
    time.sleep(1)