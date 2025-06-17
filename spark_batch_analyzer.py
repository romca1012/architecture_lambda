from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, to_timestamp, date_format

# Initialisation de Spark
spark = SparkSession.builder \
    .appName("BatchLogAnalyzer") \
    .getOrCreate()

# Lecture des logs streamés
df = spark.read.parquet("data/logs_streaming")

# Convertir le champ timestamp en format Timestamp Spark
df = df.withColumn("datetime", to_timestamp(col("timestamp")))

# 🔹 1. Connexions par IP (en filtrant les nulls)
ip_counts = df.filter(col("ip").isNotNull()) \
              .groupBy("ip") \
              .agg(count("*").alias("nb_connexions")) \
              .orderBy(col("nb_connexions").desc())

# 🔹 2. Connexions par user agent (navigateur)
agent_counts = df.groupBy("user_agent") \
                 .agg(count("*").alias("nb_connexions")) \
                 .orderBy(col("nb_connexions").desc())

# 🔹 3. Connexions par minute
minute_counts = df.withColumn("minute", date_format("datetime", "yyyy-MM-dd HH:mm")) \
                  .groupBy("minute") \
                  .agg(count("*").alias("nb_connexions")) \
                  .orderBy("minute")

# 📁 Sauvegarde des résultats
ip_counts.write.mode("overwrite").csv("data/batch_results/connexions_par_ip", header=True)
agent_counts.write.mode("overwrite").csv("data/batch_results/connexions_par_user_agent", header=True)
minute_counts.write.mode("overwrite").csv("data/batch_results/connexions_par_minute", header=True)

print("✅ Analyse batch terminée avec succès !")

spark.stop()
