import cv2, easyocr, torch
import re

from camera_selector import select_camera 
from resources import folder, saveImages

# Carpeta para guardar las imágenes
save_folder     = folder()
selected_camera = select_camera()

# Si no se ha seleccionado ninguna cámara, salir del programa
if selected_camera is None:
    exit(1)

# Inicializamos el lector de EasyOCR
reader = easyocr.Reader(['es'])  # 'es' para español, puedes cambiar el idioma si lo prefieres

# Abrir la cámara seleccionada
cap = cv2.VideoCapture(selected_camera)

# Verificar si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Ancho de la imagen
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto de la imagen
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Ancho de la imagen
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Alto de la imagen

plate_pattern = re.compile(r'^[A-Z]\d[A-Z]-\d{3}$')

while True:
    # Capturamos un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error al capturar la imagen")
        break

    # Convertimos la imagen a escala de grises (opcional pero recomendado)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Usamos EasyOCR para leer el texto de la imagen
    result = reader.readtext(gray)

    # Dibujamos los resultados en la imagen
    for detection in result:
        # Detección contiene [coordenadas del cuadro, texto, nivel de confianza]
        text = detection[1]
        # print(detection[0])
        print(detection[1])

        if plate_pattern.match(text):
            # timestamp = cv2.getTickCount()  # Usamos un timestamp para el nombre del archivo
            # cv2.imwrite(f"placa_detectada_{timestamp}.jpg", frame)
            path_save = saveImages(text, save_folder)
            # Si no es un duplicado, guardar la nueva imagen
            if path_save:
                # Guardar la imagen del fotograma con la placa detectada
                cv2.imwrite(path_save, frame)  # Guardamos la imagen


            top_left = tuple(map(int, detection[0][0]))  # Convertir a enteros
            bottom_right = tuple(map(int, detection[0][2]))  # Convertir a enteros
            # Dibujamos un rectángulo alrededor del texto detectado
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            # Mostramos el texto detectado
            cv2.putText(frame, detection[1], top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            

    # Mostrar el frame con los resultados en tiempo real
    cv2.imshow("Placa Detectada", frame)
    # time.sleep(2)  # Ajusta este valor para experimentar con la cantidad de fotogramas por segundo

    # Salir si presionas la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
torch.cuda.empty_cache()