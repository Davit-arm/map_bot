import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import random
import requests
class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path, cities):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        random_color = random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        for city in cities:
            coordinates = self.get_coordinates(city)
            if coordinates:
                lat, lng = coordinates
                plt.plot([lng], [lat], color=random_color, linewidth = 5, marker='.', transform=ccrs.Geodetic())
                plt.text(lng + 3, lat + 12, city, horizontalalignment='left', transform=ccrs.Geodetic())
        plt.savefig(path)
        plt.close()
        
    def draw_distance(self, city1, city2):
        city1_cords = self.get_coordinates(city1)
        city2_cords = self.get_coordinates(city2)  # Прушков
        random_color = random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        ax.stock_img()
        plt.plot([city1_cords[1], city2_cords[1]], [city1_cords[0], city2_cords[0]],
         color= random_color , linewidth=2, marker='o',
         transform=ccrs.Geodetic(),  # Используем геодезическую проекцию для преобразования координат
         )
        plt.text(city1_cords[1] + 3, city1_cords[0] + 12, city1,
         horizontalalignment='left',  # Горизонтальное выравнивание текста
         transform=ccrs.Geodetic()  # Используем геодезическую проекцию для преобразования координат
         )
        plt.text(city2_cords[1] + 3, city2_cords[0] + 12, city2,
         horizontalalignment='left',  # Горизонтальное выравнивание текста
         transform=ccrs.Geodetic()  # Используем геодезическую проекцию для преобразования координат
         )
        plt.savefig(f'{city1}_{city2}_distance.png')
        plt.close()

    def get_time(self, timezone: str):
        url = f"https://www.timeapi.io/api/Time/current/zone?timeZone={timezone}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json().get("dateTime") 


    #data = get_time("Europe/Paris")
    #print("Current time in Paris:", data["dateTime"])
if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_user_table()
