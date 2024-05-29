import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from functions import Config
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generar una clave secreta segura

#Coment test
# Ruta base para los archivos CSV
base_csv_path = 'Datasets'
#holi prueba

# Diccionario para las rutas de los archivos CSV
datasets = {
    "basic_stats": os.path.join(base_csv_path, "Basic_Stats.csv"),
    "Career_Stats_Offensive_Line": os.path.join(base_csv_path, "Career_Stats_Offensive_Line.csv"),
    "Career_Stats_Defensive": os.path.join(base_csv_path, "Career_Stats_Defensive.csv"),
    "Game_Logs_Quarterback": os.path.join(base_csv_path, "Game_Logs_Quarterback.csv"),
    "Game_Logs_Wide_Receiver_and_Tight_End": os.path.join(base_csv_path, "Game_Logs_Wide_Receiver_and_Tight_End.csv"),
    "Game_Logs_Runningback": os.path.join(base_csv_path, "Game_Logs_Runningback.csv"),
    "Game_Logs_Offensive_Line": os.path.join(base_csv_path, "Game_Logs_Offensive_Line.csv"),
    "Game_Logs_Defensive_Lineman": os.path.join(base_csv_path, "Game_Logs_Defensive_Lineman.csv"),
    "Career_Stats_Kick_Return": os.path.join(base_csv_path, "Career_Stats_Kick_Return.csv")
}

# URLs de las estadísticas
urls = {
    "Passing_Yards": "https://www.nfl.com/stats/player-stats/category/passing/2023/reg/all/passingyards/desc",
    "Rushing_Yards": "https://www.nfl.com/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc",
    "Receiving_Yards": "https://www.nfl.com/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc",
    "Interceptions": "https://www.nfl.com/stats/player-stats/category/interceptions/2023/reg/all/defensiveinterceptions/desc",
    "Punt_Return_Yards": "https://www.nfl.com/stats/player-stats/category/punt-returns/2023/reg/all/puntreturnsaverageyards/desc",
    "Defense_Passing_Yards" : "https://www.nfl.com/stats/team-stats/defense/passing/2023/reg/all",
    "Defense_Rushing_Yards" : "https://www.nfl.com/stats/team-stats/defense/rushing/2023/reg/all",
    "Defense_Scoring" : "https://www.nfl.com/stats/team-stats/defense/scoring/2023/reg/all",
    "Interception_by_Team" :  "https://www.nfl.com/stats/team-stats/defense/interceptions/2023/reg/all",
    "Fumbles_by_Team" :  "https://www.nfl.com/stats/team-stats/defense/fumbles/2023/reg/all"
}

# Crear el directorio de salida si no existe
output_dir = 'Scraping_CSV'
os.makedirs(output_dir, exist_ok=True)

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def extract_data(soup):
    table = soup.find('table')  # Asegúrate de que esto encuentre la tabla correcta
    headers = [th.text.strip() for th in table.find_all('th')]
    rows = []

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        rows.append(cols)

    return headers, rows

def save_to_csv(headers, rows, filename):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

def scrape_data(category):
    url = urls.get(category)
    if url:
        soup = get_soup(url)
        headers, rows = extract_data(soup)
        save_to_csv(headers, rows, f"{category}.csv")
        return f"Data for {category} saved successfully."
    else:
        return f"Error: Invalid category {category}."

@app.route("/")
def home():
    return render_template("team.html")

@app.route("/team")
def team():
    return render_template("team.html")

#---------------------------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------------------------

@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    if request.method == "POST":
        category = request.form.get("category")
        if category:
            headers, rows = Config.scrape_data(category)  # Modifica esta línea para obtener los encabezados y las filas
            if headers and rows:
                return render_template("scrape.html", categories=Config.urls.keys(), headers=headers, rows=rows)
            else:
                flash("Error: No se pudieron extraer los datos.")
                return redirect(url_for('scrape'))
    return render_template("scrape.html", categories=Config.urls.keys())

#---------------------------------------------------------------------------------------------------------------------------

@app.route("/chart_current_status", methods=["GET", "POST"])
def chart():
    if request.method == "POST":
        experience = request.form.get("experience")
        status = request.form.get("status")
        filtered_data = Config.load_and_filter_data(experience, status)
        Config.plot_pie_chart(filtered_data)
        
        headers = filtered_data.columns.tolist()
        rows = filtered_data.values.tolist()
        
        return render_template("chart_current_status.html", headers=headers, rows=rows)
    
    return render_template("chart_current_status.html")

#---------------------------------------------------------------------------------------------------------------------------

@app.route('/college')
def college_top_worst():
    # Cargar el conjunto de datos
    data = pd.read_csv('Datasets/Basic_Stats.csv')
    
    # Determinar si mostrar el top 10 con más o menos jugadores
    filter_value = request.args.get('filter', 'Top')
    
    # Llamar a la función correspondiente para generar la gráfica
    if filter_value == 'Top':
        graph_path = Config.generate_top_nfl_player_graph(data)
    elif filter_value == 'Least':
        graph_path = Config.generate_least_nfl_player_graph(data)
    else:
        raise ValueError("Invalid filter value")
    
    return render_template('college.html', graph_path=graph_path)

#---------------------------------------------------------------------------------------------------------------------------

@app.route('/nfl_teams')
def team_top_worst():
    # Cargar el conjunto de datos
    data = pd.read_csv('Scraping_CSV/Defense_Rushing_Yards.csv')
    
    # Determinar si mostrar el top 10 con más o menos jugadores
    filter_value = request.args.get('filter', 'Top')
    
    # Llamar a la función correspondiente para generar la gráfica
    if filter_value == 'Top':
        graph_path = Config.generate_top_nfl_team_graph(data)
    elif filter_value == 'Least':
        graph_path = Config.generate_least_nfl_team_graph(data)
    else:
        raise ValueError("Invalid filter value")
    
    return render_template('nfl_teams.html', graph_path=graph_path)

#---------------------------------------------------------------------------------------------------------------------------

@app.route('/nfl_teams_pass')
def team_top_worst_pass():
    # Cargar el conjunto de datos
    data = pd.read_csv('Scraping_CSV/Defense_Passing_Yards.csv')
    
    # Determinar si mostrar el top 10 con más o menos jugadores
    filter_value = request.args.get('filter', 'Top')
    
    # Llamar a la función correspondiente para generar la gráfica
    if filter_value == 'Top':
        graph_path = Config.generate_top_nfl_team_graph_pass(data)
    elif filter_value == 'Least':
        graph_path = Config.generate_least_nfl_team_graph_pass(data)
    else:
        raise ValueError("Invalid filter value")
    
    return render_template('nfl_teams_pass.html', graph_path=graph_path)

#---------------------------------------------------------------------------------------------------------------------------

@app.route("/calendar", methods=["GET", "POST"])
def mostrar_tabla():
    archivo_csv = 'Scraping_CSV/Calendar.csv'  # Ruta del archivo Calendar.csv
    df = Config.cargar_datos_desde_csv(archivo_csv)

    equipos = df['TEAM'].unique()
    semanas = df.columns[2:]

    equipo_seleccionado = request.form.get('equipo')
    semana_seleccionada = request.form.get('semana')

    if equipo_seleccionado:
        df = df[df['TEAM'] == equipo_seleccionado]

    if semana_seleccionada:
        df = df[['TEAM', semana_seleccionada]]

    tabla_html = df.to_html(classes='w3-table w3-bordered w3-striped w3-hoverable', index=False)

    return render_template("calendar.html", tabla_html=tabla_html, equipos=equipos, semanas=semanas)

#---------------------------------------------------------------------------------------------------------------------------

@app.route('/eficiencia_rush')
def mostrar_resultados():
    jugadores = []
    with open('Scraping_CSV/rushing_yards.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            TD_actuales = int(row['TD'])
            Att_actuales = int(row['Att'])
            intentos_necesarios = Config.calcular_intentos_para_TD(TD_actuales, Att_actuales)
            jugadores.append({"nombre": row['Player'], "TD": TD_actuales, "Att": Att_actuales, "intentos_necesarios": intentos_necesarios})
    return render_template('eficiencia_rush.html', jugadores=jugadores)

#---------------------------------------------------------------------------------------------------------------------------

@app.route('/eficiencia_catch')
def mostrar_resultados_pase():
    jugadores = []
    with open('Scraping_CSV/Receiving_Yards.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            TD_actuales = int(row['TD'])
            Att_actuales = int(row['Rec'])
            intentos_necesarios = Config.calcular_intentos_para_TD_por_pase(TD_actuales, Att_actuales)
            jugadores.append({"nombre": row['Player'], "TD": TD_actuales, "Att": Att_actuales, "intentos_necesarios": intentos_necesarios})
    return render_template('eficiencia_catch.html', jugadores=jugadores)

#---------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
