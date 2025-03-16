class Vehiculo:
    def __init__(self, placa, departamento_id):
        self.placa = placa
        self.departamento_id = departamento_id

    # Método para convertir el objeto a un diccionario
    def to_dict(self):
        return {
            "placa": self.placa,
            "departamento_id": self.departamento_id,
        }

    # Método para crear un objeto Usuario a partir de un documento de la base de datos
    @classmethod
    def from_dict(cls, data):
        return cls(
            placa=data["placa"],
            departamento_id=data["departamento_id"],
        )
