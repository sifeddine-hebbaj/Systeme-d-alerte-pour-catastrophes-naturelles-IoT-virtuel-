import paho.mqtt.client as mqtt
import time
import random

# MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# loopMQTT
client.loop_start()

while True:
    # Water Level
    water_level = random.uniform(0, 100)
    client.publish("sensors/waterlevel", water_level)
    print("Sent water level:", water_level)
    
    # Flood Level
    flood_level = random.uniform(0, 50)
    client.publish("sensors/floodlevel", flood_level)
    print("Sent flood level:", flood_level)
    
    # Fire Sensor (0 = no fire, 1 = fire detected)
    fire_status = random.choice([0, 1])
    client.publish("sensors/fire", fire_status)
    print("Sent fire status:", fire_status)
    
    time.sleep(5)
