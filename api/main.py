from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="Lambda Log API")

# Répertoire des résultats
BASE_PATH = "data/batch_results"

def read_csv_result(path):
    files = [f for f in os.listdir(path) if f.endswith(".csv")]
    if not files:
        return []
    df = pd.read_csv(os.path.join(path, files[0]))
    return df.to_dict(orient="records")

@app.get("/ip-stats")
def ip_stats():
    return read_csv_result(os.path.join(BASE_PATH, "connexions_par_ip"))

@app.get("/user-agent-stats")
def user_agent_stats():
    return read_csv_result(os.path.join(BASE_PATH, "connexions_par_user_agent"))

@app.get("/minute-stats")
def minute_stats():
    return read_csv_result(os.path.join(BASE_PATH, "connexions_par_minute"))
