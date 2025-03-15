import os, time
from datetime import datetime

def folder():
    current_date = datetime.now().strftime("%d%b%y").upper()
    # Carpeta para guardar las imágenes (formato de la fecha)
    save_folder = f'./placas_guardadas/{current_date}'
    # Crear la carpeta si no existe
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    return save_folder

def saveImages(text, path):
    MINUTOS = 1
    # Intervalo de tiempo en segundos
    time_threshold = MINUTOS * 60
    current_time    =   time.time()
    timestamp       =   datetime.now().strftime("%Y%m%d_%H%M%S")
    filename        =   f"{text}_{timestamp}.jpg"
    file_path       =   os.path.join(path, filename)

    plate_base_name = text
    files_in_folder = os.listdir(path)
    duplicate_found = False

    for file in files_in_folder:
        # Comprobar si el nombre de archivo contiene la placa
        if plate_base_name in file:
            # Obtener la fecha de creación del archivo
            file_creation_time = os.path.getctime(os.path.join(path, file))
            current_time = time.time()
            time_difference = current_time - file_creation_time

            # Si la imagen ya existe dentro del umbral de minutos, no la guardamos
            if time_difference < time_threshold:
                duplicate_found = True
                print(f"¡Duplicado! La imagen de {text} ya existe dentro del rango de {MINUTOS} minutos.")
                break

    # Si no es un duplicado, guardar la nueva imagen
    if not duplicate_found:
        print(f"Imagen guardada como: {filename}")
        return file_path
    return False