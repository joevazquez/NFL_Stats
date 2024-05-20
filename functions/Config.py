# Importamos las Librerías que vamos a utilizar para el desarollo del proyecto
import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
import schedule
import time

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

def save_to_log(category, status):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = [log_time, category, status]
    with open(os.path.join(log_dir, 'logs.csv'), 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(log_data)

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

# Función para realizar el web scraping para todas las categorías
def scrape_all_data():
    for category in urls:
        scrape_data(category)

# Programar la tarea de web scraping para que se ejecute todos los martes a las 10 a.m.
schedule.every().tuesday.at("10:00").do(scrape_all_data)

# Ejecutar el ciclo principal para que la programación de tareas funcione correctamente
while True:
    schedule.run_pending()
    time.sleep(1)