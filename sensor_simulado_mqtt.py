import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # Import necessário para a v2.0
import time
import random

# --- CONFIGURAÇÕES ---
BROKER = "broker.hivemq.com"
TOPIC_STATUS = "projeto/giovana/sensor01/status"
TOPIC_DATA = "projeto/giovana/sensor01/temperatura"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Conectado ao Broker!")
        # [RETAIN FLAG]
        client.publish(TOPIC_STATUS, "online", qos=1, retain=True)
    else:
        print(f"Falha na conexão. Código: {reason_code}")


client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="Sensor_Python_Demo")
client.on_connect = on_connect

# 2. [LAST WILL AND TESTAMENT]
client.will_set(TOPIC_STATUS, payload="offline", qos=1, retain=True)

# 3. Conexão
client.connect(BROKER, 1883, keepalive=10) 
client.loop_start()

try:
    print("Sensor rodando... (Pressione Ctrl+C para encerrar normalmente)")
    while True:
        temp = round(random.uniform(20, 30), 2)
        
        # 4. [RETAIN FLAG nos DADOS]
        client.publish(TOPIC_DATA, payload=str(temp), qos=1, retain=True)
        
        print(f"Temperatura enviada: {temp}°C")
        time.sleep(10)

except KeyboardInterrupt:
    print("\nEncerrando via software...")
    client.publish(TOPIC_STATUS, "offline", qos=1, retain=True)
    client.disconnect()
    client.loop_stop()