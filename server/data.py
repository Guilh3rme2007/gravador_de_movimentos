# conexao com os dados
import sqlite3
import csv
import cv2
from pathlib import Path

def createDB():
    connection = sqlite3.connect('mydatabase.db')

    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fileSprint (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS savedCameras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        camera_name TEXT NOT NULL,
        ip_url TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def searchFile():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()

    search_name = input('Digite o nome do arquivo: ')
    
    cursor.execute('SELECT * FROM fileSprint WHERE name = ?', (search_name,))

    results = cursor.fetchall()
    if results:
        for line in results:
               print(f"ID: {line[0]} | Nome: {line[1]} | Criado em: {line[2]}")
    else:
        print("Nenhum registro encontrado no banco de dados.")
        
    connection.close()

def showFiles():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM fileSprint')

    results = cursor.fetchall()
    if results:
        for line in results:
                print(f"ID: {line[0]} | Nome: {line[1]} | Criado em: {line[2]}")
    else:
        print("Nenhum registro encontrado no banco de dados.")
        
    connection.close()


def newSprint(camera):
    directory_principal = Path('records').resolve()
    directory_principal.mkdir(parents=True, exist_ok=True)

    file_name = input('Digite o nome do diretório principal:  ')
    sprint_name = input('Digite o nome da Sprint:  ')
    name_register = f"{file_name}/{sprint_name}"

    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO fileSprint (name) VALUES (?)', (name_register,))
    connection.commit()
    connection.close()

    directory = directory_principal / file_name
    directory.mkdir(parents=True, exist_ok=True)

    path_video = directory/ f"{sprint_name}_video.mp4"
    path_csv = directory/f"{sprint_name}_dados.csv"

    return str(path_video), str(path_csv)


