from pygrabber.dshow_graph import FilterGraph

def list_cameras():
    graph = FilterGraph()
    dispositivos = graph.get_input_devices()
    
    if dispositivos:
        for idx, dispositivo in enumerate(dispositivos):
            print(f"Cámara {idx}: {dispositivo}")
        return dispositivos
    else:
        print("No se encontraron cámaras disponibles.")
        return []

# Función para seleccionar la cámara
def select_camera():
    cameras = list_cameras()

    if not cameras:
        print("No se detectaron cámaras disponibles.")
        return None

    # Pedir al usuario que seleccione una cámara
    while True:
        try:
            seleccion = int(input("Selecciona el número de la cámara con la que deseas iniciar: "))
            
            # Verificar si el número ingresado es válido
            if seleccion >= len(cameras) or seleccion < 0:
                print("Selección inválida. Por favor selecciona un número dentro de la lista.")
            else:
                # Retornar el índice de la cámara seleccionada
                return seleccion
        
        except ValueError:
            print("Por favor ingresa un número válido de la lista.")

# Ejemplo de uso
# se ejecuta cuando el script se ejecuta directamente desde la termina
# python camera_selector.py
if __name__ == "__main__":
    camera_id = select_camera()
    print(f"Cámara seleccionada: {camera_id}")
