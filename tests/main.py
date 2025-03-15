import cv2
import easyocr

# Inicializamos el lector de EasyOCR
reader = easyocr.Reader(['es'])  # 'es' para español, pero puedes usar otro idioma si lo prefieres

# Cargar la imagen con OpenCV
# image_path = './images/placa_1.png'
image_path = './images/placa_2.jpg'

image = cv2.imread(image_path)

# Convertir la imagen a escala de grises (opcional pero recomendado para mejorar el OCR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Usamos EasyOCR para leer el texto de la imagen
result = reader.readtext(gray)

# Imprimir el texto encontrado
for detection in result:
    print(f'Texto detectado: {detection[1]}')

# Mostrar la imagen (opcional)
cv2.imshow("Placa Detectada", image)
cv2.waitKey(0)
cv2.destroyAllWindows()