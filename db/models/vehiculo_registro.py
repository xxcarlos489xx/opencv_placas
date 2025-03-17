import time
from datetime import datetime

class VehiculoRegistro:
    def __init__(self, placa, confianza):
        self.placa          =   placa
        self.confianza      =   confianza
        self.fecha          =   datetime.now().strftime("%Y-%m-%d")  # Fecha en formato "YYYY-MM-DD"
        self.hora           =   datetime.now().strftime("%H:%M:%S")  # Hora en formato "HH:MM:SS"
        self.tiempo_unix    =   int(time.time())  # Tiempo Unix en segundos

    # Método para convertir el objeto a un diccionario
    def to_dict(self):
        return {
            "placa": self.placa,
            "confianza": self.confianza,
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