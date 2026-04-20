import paho.mqtt.client as mqtt
import time
import random

# --- CONFIGURAÇÕES ---
BROKER = "mqtt.eclipseprojects.io"
TOPIC_STATUS = "projeto/giovana/sensor01/status"
TOPIC_DATA = "projeto/giovana/sensor01/temperatura"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao Broker!")
        # [RETAIN FLAG] - Publicamos que estamos ONLINE com retain=True
        # Assim, qualquer monitor que abrir depois saberá o status atual.
        client.publish(TOPIC_STATUS, "online", qos=1, retain=True)
    else:
        print(f"Falha na conexão, código: {rc}")

# 1. Instância do Cliente
client = mqtt.Client("Sensor_Python_Demo")
client.on_connect = on_connect

# 2. [LAST WILL AND TESTAMENT]
# Configuramos ANTES de conectar. Se o sensor "morrer", o broker publica isso.
# Usamos retain=True para que o status "offline" fique gravado no tópico.
client.will_set(TOPIC_STATUS, payload="offline", qos=1, retain=True)

# 3. Conexão
client.connect(BROKER, 1883, keepalive=10) # Keepalive baixo para o teste ser rápido
client.loop_start()

try:
    print("Sensor rodando...")
    while True:
        temp = round(random.uniform(20, 30), 2)
        
        # 4. [RETAIN FLAG nos DADOS]
        # Publicamos a temperatura com retain=True para que o Dashboard
        # não fique vazio ao ser iniciado.
        client.publish(TOPIC_DATA, payload=temp, qos=1, retain=True)
        
        print(f"🌡️ Temperatura enviada: {temp}°C")
        time.sleep(10)

except KeyboardInterrupt:
    print("\nEncerrando via software...")
    # Se encerramos via código, avisamos que estamos offline manualmente
    client.publish(TOPIC_STATUS, "offline", qos=1, retain=True)
    client.disconnect()
    client.loop_stop()
