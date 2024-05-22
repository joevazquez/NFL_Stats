# Importamos las Librerías que vamos a utilizar para el desarollo del proyecto
import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
import schedule
import time
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd
import io

#Declaraciones para poder ejecutar el código

# Delclarando las variables para poder hacer web scraping a la página https://www.nfl.com/
url_passing_yards = "https://www.nfl.com/stats/player-stats/category/passing/2023/reg/all/passingyards/desc"
url_rushing_yards = "https://www.nfl.com/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc"
url_reciving_yards = "https://www.nfl.com/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc"
url_interceptions = "https://www.nfl.com/stats/player-stats/category/interceptions/2023/reg/all/defensiveinterceptions/desc"
url_punt_return_yards = "https://www.nfl.com/stats/player-stats/category/punt-returns/2023/reg/all/puntreturnsaverageyards/desc"


# Definimos las variables para las lecturas de los csv
BasicStats = "Basic_Stats.csv"
Defensive = "Career_Stats_Defensive.csv"
KickReturn = "Career_Stats_Kick_Return.csv"
Offensive = "Career_Stats_Offensive_Line.csv"
PassingYards =  "Career_Stats_Passing.csv"
ReceivingYards =  "Career_Stats_Receiving.csv"
RushingYards =  "Career_Stats_Rushing.csv"

# Historicos en el dataset
LogsKickers =  "Game_Logs_Kickers.csv"
LogsDefensive = "Game_Logs_Defensive_Lineman.csv"
LogsOffensive =  "Game_Logs_Offensive_Line.csv"
LogsQB =  "Game_Logs_Quarterback.csv"
LogsRB =  "Game_Logs_Runningback.csv"
LogsWRandTE =  "Game_Logs_Wide_Receiver_and_Tight_End.csv"

# URLs de las estadísticas para alimentar el Web Scraping
urls = {
    "passing_yards": "https://www.nfl.com/stats/player-stats/category/passing/2023/reg/all/passingyards/desc",
    "rushing_yards": "https://www.nfl.com/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc",
    "receiving_yards": "https://www.nfl.com/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc",
    "interceptions": "https://www.nfl.com/stats/player-stats/category/interceptions/2023/reg/all/defensiveinterceptions/desc",
    "punt_return_yards": "https://www.nfl.com/stats/player-stats/category/punt-returns/2023/reg/all/puntreturnsaverageyards/desc"
}

# Crear el directorio de salida si no existe
output_dir = 'Scraping_CSV'
os.makedirs(output_dir, exist_ok=True)

# Crear el directorio para los logs si no existe
log_dir = 'Logs'
os.makedirs(log_dir, exist_ok=True)

# Se crea código para hacer la sopa y hacer la extracción de la data

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

# Se crea código para escribir los logs 

def save_to_csv(headers, rows, filename):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

def save_to_log(category, status):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = [log_time, category, status]
    with open(os.path.join(log_dir, 'logs.csv'), 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(log_data)

# Se crea código para hacer el Web Scraping

def scrape_data(category):
    url = urls.get(category)
    if url:
        try:
            soup = get_soup(url)
            headers, rows = extract_data(soup)
            # Guardar los datos en un archivo CSV
            save_to_csv(headers, rows, f"{category}.csv")
            # Guardar el registro en el archivo de logs
            save_to_log(category, "Success")
            # Devolver los datos extraídos
            return headers, rows
        except Exception as e:
            # Si ocurre algún error, guardar el registro de error en el archivo de logs
            save_to_log(category, f"Error: {str(e)}")
            return None, None
    else:
        return None, None

def scrape_all_data():
    for category in urls:
        scrape_data(category)

# Programar la tarea de web scraping para que se ejecute todos los martes a las 10 a.m.
schedule.every().thursday.at("10:00").do(scrape_all_data)

# Mantener el servicio activo ejecutando un bucle infinito en un hilo separado
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

# Iniciar el planificador al ejecutar el archivo
start_scheduler()

# Dirección para poder obtener el Dataset
path_csv_read = 'Datasets/Basic_Stats.csv'

# Se crea los filtros para poder tener la funcionalidad de la tabla
def load_and_filter_data(experience, status):
    df = pd.read_csv(path_csv_read)
    
    # Filtrar por experiencia si se proporciona
    if experience:
        experience_map = {
            '0 Season': '0 Season',
            '1 Season': '1 Season',
            '2nd season': '2nd season',
            '3th season': ['3 Seasons', '3th season', '3rd season'],
            '4th season': ['4 Seasons', '4th season'],
            '5th season': ['5 Seasons', '5th season'],
            '6th season': ['6 Seasons', '6th season'],
            '7th season': ['7 Seasons', '7th season'],
            '8th season': ['8 Seasons', '8th season'],
            '9th season': ['9 Seasons', '9th season'],
            '10th season': ['10 Seasons', '10th season'],
            '11th season': ['11 Seasons', '11th season'],
            '13th season': ['13 Seasons', '13th season'],
            '14th season': ['14 Seasons', '14th season'],
            '15th season': ['15 Seasons', '15th season'],
            '16th season': ['16 Seasons', '16th season'],
            '17th season': ['17 Seasons', '17th season'],
            '18th season': ['18 Seasons', '18th season'],
            '19th season': ['19 Seasons', '19th season'],
            '20th season': ['20 Seasons', '20th season'],
            '21th season': ['21 Seasons', '21th season'],
            '22th season': ['22 Seasons', '22th season'],
            '23th season': ['23 Seasons', '23th season'],
            '24th season': ['24 Seasons', '24th season'],
            '25th season': ['25 Seasons', '25th season']
        }
        
        if experience in experience_map:
            if experience == '0 Season':
                filtered_by_experience = df[df['Experience'] == '0 Season']

            elif isinstance(experience_map[experience], list):
                filtered_by_experience = df[df['Experience'].isin(experience_map[experience])]
            else:
                filtered_by_experience = df[df['Experience'] == experience_map[experience]]
        else:
            filtered_by_experience = df  # No hay filtro de experiencia
    else:
        filtered_by_experience = df  # No se proporcionó filtro de experiencia
    
    # Filtrar por estado si se proporciona
    if status:
        status_map = {
            'Active': 'Active',
            'Retired': 'Retired',
            'Injured Reserve': 'Injured Reserve',
            'Physically Unable to Perform': 'Physically Unable to Perform',
            'Suspended': 'Suspended',
            'Unsigned Free Agent': 'Unsigned Free Agent'
        }
        
        if status == 'All Status':
            filtered_by_status = filtered_by_experience
        elif status in status_map:
            filtered_by_status = filtered_by_experience[filtered_by_experience['Current Status'] == status_map[status]]
        else:
            filtered_by_status = filtered_by_experience  # No hay filtro de estado válido
    else:
        filtered_by_status = filtered_by_experience  # No se proporcionó filtro de estado
    
    return filtered_by_status


# Crea la gráfica de Status vs Experiencia
def plot_pie_chart(data):
    plt.figure(figsize=(8, 8))  # Ajusta el tamaño de la figura si es necesario
    status_counts = data['Current Status'].value_counts()
    
    # Generar el gráfico de pastel sin etiquetas
    patches, texts, autotexts = plt.pie(status_counts, autopct='%1.1f%%', startangle=60)
    
    # Agregamos las etiquetas de estado y la cuenta de jugadores
    labels = ['{} - {}'.format(status, count) for status, count in zip(status_counts.index, status_counts)]
    plt.legend(patches, labels, loc="center left", bbox_to_anchor=(1, 0.5))
    
    plt.title('Distribución de jugadores por estado actual')
    plt.tight_layout()
    plt.savefig('static/plot.png')  # Guardamos la gráfica en un archivo
    plt.close()  # Cerramos la figura para evitar problemas de sobrecarga de gráficos


def generate_top_nfl_player_graph(data):
    # Filtrar los jugadores activos
    active_players = data[data['Current Status'] == 'Active']

    # Obtener las universidades con más jugadores activos
    top_colleges = active_players['College'].value_counts().nlargest(10)

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    top_colleges.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Universidades con más jugadores activos en la NFL')
    plt.xlabel('Universidad')
    plt.ylabel('Número de jugadores activos')
    plt.tight_layout()
    plt.savefig('static/top_colleges.png')
    plt.close()

    return 'static/top_colleges.png'


def generate_least_nfl_player_graph(data):
    # Filtrar los jugadores activos
    active_players = data[data['Current Status'] == 'Active']

    # Obtener las universidades con menos jugadores activos
    least_colleges = active_players['College'].value_counts().nsmallest(10)

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    least_colleges.plot(kind='bar', color='lightcoral')
    plt.title('Top 10 Universidades con menos jugadores activos en la NFL')
    plt.xlabel('Universidad')
    plt.ylabel('Número de jugadores activos')
    plt.tight_layout()
    plt.savefig('static/least_colleges.png')
    plt.close()

    return 'static/least_colleges.png'


