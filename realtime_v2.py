import torch
import cv2
import re
from detector import detect_objects
from camera_selector import select_camera 
from resources import folder

# Carpeta para guardar las imágenes
save_folder     = folder()
selected_camera = select_camera()

# Si no se ha seleccionado ninguna cámara, salir del programa
# if selected_camera is None:
    # exit(1)

# Abrir la cámara seleccionada
cap = cv2.VideoCapture(selected_camera)
# cap = cv2.VideoCapture("tests/videos/video.mp4")

# Verificar si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Ancho de la imagen
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto de la imagen
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Ancho de la imagen
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Alto de la imagen

placa_pattern = re.compile(r'^[A-Z]\d[A-Z]-\d{3}$')

ret, frame = cap.read()
# roi = cv2.selectROI("Seleccione la region de interes", frame, fromCenter=False, showCrosshair=True)
# x_roi, y_roi, w_roi, h_roi = roi
# cv2.destroyWindow("Seleccione la region de interes")
x_roi, y_roi, w_roi, h_roi = 0, 0, frame.shape[1], frame.shape[0]
# cv2.destroyWindow()

while cap.isOpened():
    if not ret:
        print("Error al capturar el fotograma")
        break

    # Llamar a la función de detección de objetos
    frame = detect_objects(cap, save_folder, x_roi, y_roi, w_roi, h_roi)

    # Mostrar el fotograma con las detecciones
    cv2.imshow("Mostrar lives", frame)

    # Salir si presionas la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
torch.cuda.empty_cache()