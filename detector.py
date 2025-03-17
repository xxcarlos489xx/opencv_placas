# # results = model('test1.jpg')
# from ultralytics import YOLO
# model = YOLO("yolo11n.pt")
# print(model.names)
# # for result in results:
# #     result.show()
# exit(1)
from config.class_translation import class_translation 
from ultralytics import YOLO
import cv2
import easyocr
import re
# from paddleocr import PaddleOCR
from resources import saveImages
from db.repository.vehiculo_registro import VehiculoRegistroRepository
from db.models.vehiculo_registro import VehiculoRegistro
from db.repository.vehiculo import VehiculoRepository
from cvzone.Utils import cornerRect, putTextRect

permitidos = {
    0: "person",
    2: "car",
    # 3: "motorcycle",
    # 5: "bus",
    # 7: "truck",
}

model_yolo = YOLO("yolo11n.pt")
model_yolo.to('cpu')

model_placa = YOLO("license_plate_detector.pt")
model_placa.to('cpu')

reader = easyocr.Reader(['es'])  # 'es' para español, puedes cambiar el idioma si lo prefieres
# ocr = PaddleOCR(use_angle_cls=True, lang='es')  # Puedes cambiar el idioma si es necesario

placa_pattern = re.compile(r'^[A-Z][A-Z0-9][A-Z]-\d{3}$')

def detect_objects(cap, folder_images, x_roi, y_roi, w_roi, h_roi):
    """
    Detecta objetos en el fotograma usando YOLO y dibuja las cajas delimitadoras y etiquetas traducidas.
    """
    ret, frame  =   cap.read()
    roi_frame   =   frame[y_roi:y_roi + h_roi, x_roi:x_roi + w_roi].copy()
    results     =   model_yolo.track(roi_frame, persist=True)

    for result in results:
        # class_names = results[0].names#lista las clases de objetos disponibles
        # print("class_names ",class_names)

        if result.boxes.id is None:
            continue

        for box, class_id, track_id, confidence in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.id, result.boxes.conf):
            class_id = int(class_id)
            track_id = int(track_id)

            if class_id in permitidos:
                confidence      =   confidence.cpu().numpy()
                x1, y1, x2, y2  =   map(int, box.cpu().numpy())
                x1 += x_roi
                x2 += x_roi
                y1 += y_roi
                y2 += y_roi

                # class_name = permitidos.get(class_id)
                class_name = model_yolo.names.get(class_id)
                translated_name = class_translation.get(class_name)

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {track_id} {translated_name} : {confidence:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                vehicle_crop = frame[y1:y2, x1:x2].copy()
                plates_result = model_placa(vehicle_crop)

                for result in plates_result:
                    # if result.boxes.id is None:
                    #     continue

                    for box in result.boxes.xyxy:
                        px1, py1, px2, py2 = map(int, box.cpu().numpy())
                        px1 += x1
                        px2 += x1
                        py1 += y1
                        py2 += y1

                        # cv2.rectangle(frame, (int(px1), int(py1)), (int(px2), int(py2)), (0, 255, 0), 2)
                        # cv2.putText(frame, f"Plate {track_id}", (int(px1), int(py1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        placa_crop = frame[py1:py2, px1:px2].copy()
                        # cv2.imwrite("mi_placa.jpg", placa_crop)#save image
                        # cv2.imwrite("mi_vehiculo.jpg", vehicle_crop)#save image
                        placa_crop = cv2.resize(placa_crop, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)
                        placa_gray = cv2.cvtColor(placa_crop, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite("mi_placa.jpg", placa_crop)#save image

                        # Usamos EasyOCR para leer el texto de la imagen
                        read_placa = reader.readtext(placa_gray)

                        # Usar PaddleOCR para leer el texto de la placa
                        # read_placa = ocr.ocr(plate_crop, cls=True)

                        for detection in read_placa:
                            # Detección contiene [coordenadas del cuadro, texto, nivel de confianza]
                            text = limpiar_texto(detection[1])
                            # confianza = round(detection[2], 2)
                            confianza = detection[2]
                            
                            # print(detection[0])
                            color_rectangulo = (0, 0, 255) #red color

                            if placa_pattern.match(text) and confianza > 0.7:
                                path_save = saveImages(text, folder_images)
                                if path_save:
                                    # Guardar el registro en mongodb
                                    repo        = VehiculoRegistroRepository()
                                    registro    = VehiculoRegistro(placa=text, confianza=confianza)
                                    inserted_id = repo.insertar(registro)
                                    # Guardar la imagen del vehiculo con la placa detectada
                                    cv2.imwrite(path_save, vehicle_crop)  # Guardamos la imagen

                                # BUSCAR PLACA EN MONGODB
                                busqueda = VehiculoRepository().obtener_por_placa(text)   
                                reporte = "VEHICULO NO AUTORIZADO"

                                if busqueda:
                                    color_rectangulo = (0, 255, 0) #green color
                                    reporte = "VEHICULO AUTORIZADO"

                                # cornerRect(frame, (int(px1), int(py1), int(px2-px1), int(py2-py1)), l=10, rt=2, colorR=(255,0,0))
                                # cornerRect(frame, (int(x1), int(y1), int(x2-x1), int(y2-y1)), l=10, rt=2, colorR=(255,0,0))
                                
                                # putTextRect(frame, f"{text}", (int(px1), int(py1) - 10), scale=0.8, thickness=2, colorR=(255, 0, 0), colorB=(255, 255, 255), border=3)
                                putTextRect(frame, f"{text}", (int(px1), int(py1) - 10), scale=1, thickness=2, colorR=(0, 0, 0), colorB=(255, 255, 255), border=3)

                                # cv2.rectangle(frame, (int(px1), int(py1)), (int(px2), int(py2)), color_rectangulo, 2)
                                cv2.putText(frame, f"{reporte}", (int(px1), int(py1) + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_rectangulo, 2)
                                # Escribimos el texto en un archivo .txt
                                with open("placas_detectadas.txt", "a") as file:
                                    file.write(text + "\n")
    return frame

def limpiar_texto(texto):
    # Usamos una expresión regular para conservar solo números, letras mayúsculas y el guion "-"
    texto_limpio = re.sub(r'[^A-Z0-9-]', '', texto)
    return texto_limpio