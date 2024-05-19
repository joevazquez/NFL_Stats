import os
from flask import Flask, render_template, request
import pandas as pd
import functions.Config as Config

app = Flask(__name__)

# Ruta base para los archivos CSV
base_csv_path = 'Datasets'

# Diccionario para las rutas de los archivos CSV
datasets = {
    "basic_stats": os.path.join(base_csv_path, Config.BasicStats),
    "Career_Stats_Offensive_Line": os.path.join(base_csv_path, Config.Offensive),
    "Career_Stats_Defensive": os.path.join(base_csv_path, Config.Defensive),
    "Game_Logs_Quarterback": os.path.join(base_csv_path, Config.LogsQB),
    "Game_Logs_Wide_Receiver_and_Tight_End": os.path.join(base_csv_path, Config.LogsWRandTE),
    "Game_Logs_Runningback": os.path.join(base_csv_path, Config.LogsRB),
    "Game_Logs_Offensive_Line": os.path.join(base_csv_path, Config.LogsOffensive),
    "Game_Logs_Defensive_Lineman": os.path.join(base_csv_path, Config.LogsDefensive),
    "Career_Stats_Kick_Return": os.path.join(base_csv_path, Config.KickReturn)
}

@app.route("/")
def home():
    return render_template("team.html")

@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/database", methods=["GET", "POST"])
def database():
    selected_dataset = request.form.get("dataset", "basic_stats")  # Default to basic_stats
    csv_file_path = datasets.get(selected_dataset, datasets["basic_stats"])
    
    # Verificar si el archivo CSV existe
    if not os.path.isfile(csv_file_path):
        return f"Error: El archivo {csv_file_path} no se encontró.", 404
    
    # Leer el archivo CSV usando pandas
    df = pd.read_csv(csv_file_path)
    
    # Convertir el DataFrame a HTML
    df_html = df.to_html(classes='w3-table w3-bordered w3-striped w3-hoverable')

    # Pasar el nombre del dataset al contexto de la plantilla
    return render_template("database.html", table_html=df_html, selected_dataset=selected_dataset.replace('_', ' '))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
