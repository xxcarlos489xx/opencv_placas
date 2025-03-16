import time
from datetime import datetime

class VehiculoRegistro:
    def __init__(self, placa):
        self.placa = placa
        self.fecha = datetime.now().strftime("%Y-%m-%d")  # Fecha en formato "YYYY-MM-DD"
        self.hora = datetime.now().strftime("%H:%M:%S")  # Hora en formato "HH:MM:SS"
        self.tiempo_unix = int(time.time())  # Tiempo Unix en segundos

    # Método para convertir el objeto a un diccionario
    def to_dict(self):
        return {
            "placa": self.placa,
            "fecha": self.fecha,
            "hora": self.hora,
            "tiempo_unix": self.tiempo_unix,
            
        }

    # Método para crear un objeto VehiculoRegistro a partir de un documento de la base de datos
    @classmethod
    def from_dict(cls, data):
        return cls(
            placa=data["placa"],
            fecha=data["fecha"],
            hora=data["hora"],
            tiempo_unix=data["tiempo_unix"]
    )