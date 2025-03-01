from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
from threading import Lock
import serial
import time

# Топики для реле
MQTT_TOPIC_RELAY_1 = "/devices/wb-mr6c_137/controls/K1/on"  
MQTT_TOPIC_RELAY_2 = "/devices/wb-mr6c_137/controls/K2/on" 
MQTT_TOPIC_RELAY_3 = "/devices/wb-mr6c_137/controls/K3/on"  
MQTT_TOPIC_RELAY_4 = "/devices/wb-mr6c_137/controls/K4/on" 
MQTT_TOPIC_RELAY_5 = "/devices/wb-mr6c_137/controls/K5/on"  
MQTT_TOPIC_RELAY_6 = "/devices/wb-mr6c_137/controls/K6/on" 

# Настройки MQTT
MQTT_BROKER = "192.168.42.1"  # Адрес MQTT брокера
MQTT_PORT = 1883              # Порт MQTT брокера

# Функция для отправки команды на реле
def set_relay(topic, state):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(topic, state)
    client.disconnect()
# Настройка последовательного порта
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Замените 'COM3' на ваш порт

def send_command(command):
    ser.write(command.encode('utf-8'))
    time.sleep(0.1)  # Даем время для обработки команды

def read_response():
    response = ser.readline().decode('utf-8').strip()
    return response

def main():
    try:
        while True:
            if ser.in_waiting > 0:
                command = read_response()
                print(f"Received command: {command}")
                
                # Пример обработки команд
                if command == '1':
                    set_relay(MQTT_TOPIC_RELAY_1, "1")
                elif command == '2':
                    set_relay(MQTT_TOPIC_RELAY_1, "0")
                elif command == '3':
                    set_relay(MQTT_TOPIC_RELAY_2, "1")
                elif command == '4':
                    set_relay(MQTT_TOPIC_RELAY_2, "0")
                elif command == '5':
                    set_relay(MQTT_TOPIC_RELAY_3, "1")
                elif command == '6':
                    set_relay(MQTT_TOPIC_RELAY_3, "0")
                # Добавьте обработку других команд по аналогии

    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        ser.close()

if __name__ == "__main__":
    main()