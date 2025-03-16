# Proyecto: Lector de Placas de Vehículos

Este proyecto utiliza Python 3.13.2 para capturar imágenes de placas de vehículos, reconocer el texto de las mismas y mostrarlo en consola usando OpenCV y EasyOCR.

## 🚀 Instalación y Configuración

### 1. Crear el entorno virtual
Para mantener las dependencias aisladas del sistema:
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
- En **Windows** (Git Bash):
```bash
source venv/Scripts/activate
```
- En **Linux/MacOS**:
```bash
source venv/bin/activate
```

### 3. Instalar dependencias
Para instalar las librerías necesarias:
```bash
pip install -r requirements.txt
```

Si deseas agregar nuevas dependencias:
```bash
pip install <nombre_libreria>
```

### 4. Actualizar `requirements.txt`
Después de instalar nuevas dependencias, actualiza el archivo:
```bash
pip freeze > requirements.txt
```

## 🖥️ Ejecución del Proyecto
Para ejecutar el programa principal
```bash
python realtime.py
```

## 👥 Restaurar el entorno en otro equipo
Cuando clones el repositorio en otra máquina, sigue estos pasos:
```bash
git clone <URL_DEL_REPO>
cd <nombre_del_proyecto>
python -m venv venv
source venv/Scripts/activate  # En Windows (Git Bash)
pip install -r requirements.txt
```
### Dependecies installed
Verificar el pytorch indicado

https://pytorch-org.translate.goog/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc

```bash
    nvidia-smi #verificar si se tiene GPU y cuda
    pip3 install opencv-python easyocr
    pip install torch==2.6.0 #only cpu
    pip3 install pygrabber

    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 #with cuda
 ```