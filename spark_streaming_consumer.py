from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .appName("KafkaSparkStreamingConsumer") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Lire depuis Kafka
df_raw = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "logs_connexions") \
    .load()

# Convertir les valeurs Kafka de binaire à string
df_string = df_raw.selectExpr("CAST(value AS STRING) as log")

# Extraire les champs du log (timestamp, ip, user-agent)
df_parsed = df_string.withColumn("timestamp", split(col("log"), " - ").getItem(0)) \
                     .withColumn("ip", split(col("log"), " - ").getItem(1)) \
                     .withColumn("user_agent", split(col("log"), " - ").getItem(2))

# Écriture en Parquet
query = df_parsed.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "./data/checkpoint") \
    .option("path", "./data/logs_streaming") \
    .outputMode("append") \
    .start()

query.awaitTermination()
