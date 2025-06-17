import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Connexion au broker Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Échantillons simulés
user_agents = ['Mozilla/5.0', 'Chrome/90.0', 'Safari/14.0', 'Edge/92.0']
ips = ['192.168.1.' + str(i) for i in range(1, 10)]

print("Démarrage de la génération de logs...")

while True:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = random.choice(ips)
    agent = random.choice(user_agents)
    log = f"{timestamp},{ip},{agent}"
    
    # Envoi dans le topic Kafka
    producer.send('logs_connexions', log.encode('utf-8'))
    print("Envoyé:", log)
    
    time.sleep(1)  # envoie 1 log/seconde
