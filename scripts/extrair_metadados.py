import os
import sqlite3
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Extrai dados EXIF da imagem."""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data["GPSInfo"] = gps_data
            else:
                # Verifica e converte valores do tipo 'IFDRational' (fração)
                if isinstance(value, tuple) and len(value) == 2:
                    value = value[0] / value[1]  # Converte a fração para um número
                exif_data[decoded] = value
    return exif_data

def get_coordinates(gps_info):
    """Converte informações GPS para latitude e longitude em graus decimais."""
    def convert_to_degrees(value):
        d, m, s = value
        return d[0] / d[1] + (m[0] / m[1]) / 60 + (s[0] / s[1]) / 3600

    lat = lon = None
    if gps_info:
        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get("GPSLatitudeRef")
        gps_longitude = gps_info.get("GPSLongitude")
        gps_longitude_ref = gps_info.get("GPSLongitudeRef")

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = convert_to_degrees(gps_latitude)
            if gps_latitude_ref != "N":
                lat = -lat
            lon = convert_to_degrees(gps_longitude)
            if gps_longitude_ref != "E":
                lon = -lon
    return lat, lon

def create_database(db_path):
    """Cria o banco de dados e a tabela, se não existirem."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata_imagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_imagem TEXT,
            data_captura TEXT,
            latitude REAL,
            longitude REAL,
            pasta TEXT,
            tamanho_mb REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_metadata(db_path, data):
    """Insere os metadados de uma imagem no banco."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metadata_imagens (
            nome_imagem, data_captura, latitude, longitude, pasta, tamanho_mb
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def process_images(base_path, db_path):
    """Processa todas as imagens do diretório."""
    create_database(db_path)
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                try:
                    image = Image.open(file_path)
                    exif_data = get_exif_data(image)
                    gps_info = exif_data.get("GPSInfo", {})
                    lat, lon = get_coordinates(gps_info)
                    data_captura = exif_data.get("DateTimeOriginal")
                    tamanho_mb = os.path.getsize(file_path) / (1024 * 1024)
                    pasta = os.path.basename(os.path.dirname(file_path))

                    insert_metadata(db_path, (
                        file,
                        data_captura,
                        lat,
                        lon,
                        pasta,
                        round(tamanho_mb, 2)
                    ))
                    print(f"Processado: {file}")

                except Exception as e:
                    print(f"Erro ao processar {file}: {e}")

if __name__ == "__main__":
    base_path = "../imagens/"  # Defina o caminho correto para suas imagens
    db_path = "imagens_metadata.db"  # Defina o caminho correto para o banco de dados
    process_images(base_path, db_path)
