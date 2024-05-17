# Importamos las Librerías que vamos a utilizar para el desarollo del proyecto
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import schedule
import time

#Declaraciones para poder ejecutar el código

# Delclarando las variables para poder hacer web scraping a la página https://www.nfl.com/
url_passing_yards = "https://www.nfl.com/stats/player-stats/category/passing/2023/reg/all/passingyards/desc"
url_rushing_yards = "https://www.nfl.com/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc"
url_reciving_yards = "https://www.nfl.com/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc"
url_interceptions = "https://www.nfl.com/stats/player-stats/category/interceptions/2023/reg/all/defensiveinterceptions/desc"
url_punt_return_yards = "https://www.nfl.com/stats/player-stats/category/punt-returns/2023/reg/all/puntreturnsaverageyards/desc"

# Declaración de las Sopas para poder hacer web Scraping por separado 

# Hacer una solicitud a la página url_passing_yards
response = requests.get(url_passing_yards)
soup_passing_yards = BeautifulSoup(response.content, 'html.parser')

# Hacer una solicitud a la página url_rushing_yards
response = requests.get(url_rushing_yards)
soup_rushing_yards = BeautifulSoup(response.content, 'html.parser')

# Hacer una solicitud a la página url_reciving_yards
response = requests.get(url_reciving_yards)
soup_reciving_yards = BeautifulSoup(response.content, 'html.parser')

# Hacer una solicitud a la página url_interceptions
response = requests.get(url_interceptions)
soup_interceptions = BeautifulSoup(response.content, 'html.parser')

# Hacer una solicitud a la página url_punt_return_yards
response = requests.get(url_punt_return_yards)
soup_return_yards = BeautifulSoup(response.content, 'html.parser')

# Definimos las variables para las lecturas de los csv
BasicStats = "/Datasets/Basic_Stats.csv"
Defensive = "/Datasets/Career_Stats_Defensive.csv"
KickReturn = "/Datasets/Career_Stats_Kick_Return.csv"
Offensive = "/Datasets/Career_Stats_Offensive_Line.csv"
PassingYards =  "/Datasets/Career_Stats_Passing.csv"
ReceivingYards =  "/Datasets/Career_Stats_Receiving.csv"
RushingYards =  "/Datasets/Career_Stats_Rushing.csv"

# Historicos en el dataset
LogsKickers =  "/Datasets/Game_Logs_Kickers.csv"
LogsDefensive = "/Datasets/Game_Logs_Defensive_Lineman.csv"
LogsOffensive =  "/Datasets/Game_Logs_Offensive_Line.csv"
LogsQB =  "/Datasets/Game_Logs_Quarterback.csv"
LogsRB =  "/Datasets/Game_Logs_Runningback.csv"
LogsWRandTE =  "/Datasets/Game_Logs_Wide_Receiver_and_Tight_End.csv"