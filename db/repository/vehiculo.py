from db.mongodb_connection_manager import MongoDBConnectionManager
from db.models.vehiculo import Vehiculo 

class VehiculoRepository:
    def __init__(self):
        # Usamos la conexión global y seleccionamos la colección específica
        db = MongoDBConnectionManager.get_db()  # Obtenemos la base de datos
        self.collection = db['vehiculos'] 

    # Método para insertar un vehiculo
    # def insertar(self, vehiculo: Vehiculo):
    #     resultado = self.collection.insert_one(vehiculo.to_dict())
    #     return resultado.inserted_id

    # Método para obtener un vehiculo por placa
    def obtener_por_placa(self, placa: str):
        data = self.collection.find_one({"placa": placa})
        if data:
            return Vehiculo.from_dict(data)
        return None

    # Método para obtener todos los vehiculos
    def lista(self):
        vehiculos = []
        for data in self.collection.find():
            vehiculos.append(Vehiculo.from_dict(data))
        return vehiculos

    # Método para eliminar un usuario por nombre
    # def eliminar(self, nombre: str):
    #     result = self.collection.delete_one({"nombre": nombre})
    #     return result.deleted_count > 0
