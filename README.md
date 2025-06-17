🌀 Lambda Log Processing – Projet d'Architecture Lambda (Kafka + Spark)
📚 Contexte
Ce projet met en œuvre une architecture Lambda pour analyser en temps réel et en batch des logs de connexions utilisateurs. Il combine Kafka, Spark Streaming, Spark Batch, et expose les résultats via une API FastAPI.

⚙️ Technologies utilisées
Kafka (Streaming des logs en temps réel)

Apache Spark 3.5.1

Streaming (consommation Kafka)

Batch (traitement et agrégation)

FastAPI (exposition des métriques)

Docker & Docker Compose

Python 3.12, Pandas, Uvicorn

Parquet pour stockage structuré

🏗️ Architecture
lua
Copier
Modifier
+------------------+        +-------------------------+        +--------------------+
|  log_generator.py|  ==>   |   Kafka (topic logs)    |  ==>   | Spark Streaming    |
|  (fichier Python)|        |                         |        | (spark_streaming_) |
+------------------+        +-------------------------+        +--------------------+
                                                                      |
                                                                      v
                                             +-------------------------------+
                                             | Parquet (data/logs_streaming) |
                                             +-------------------------------+

                                                      ⇓

                                            +----------------------+
                                            | Spark Batch Job      |
                                            | (traitement des logs)|
                                            +----------------------+
                                                      ⇓
                                             data/batch_results/
                                                      ⇓
                                             API FastAPI (3 endpoints)
🚀 Lancer le projet
1. Démarrage de l'environnement Kafka
docker-compose up -d
2. Génération des logs (envoie dans Kafka)
python log_generator.py
3. Lancement de Spark Streaming
./spark-3.5.1-bin-hadoop3/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  spark_streaming_consumer.py
4. Lancement du traitement batch
spark-shell
scala
Copier
Modifier
// Exemple :
val df = spark.read.parquet("data/logs_streaming")
val result = df.groupBy("ip").count().withColumnRenamed("count", "nb_connexions")
result.write.option("header", true).mode("overwrite").csv("data/batch_results/connexions_par_ip")
5. Lancer l'API FastAPI
uvicorn api.main:app --reload
➡️ Accéder à la documentation : http://127.0.0.1:8000/docs
