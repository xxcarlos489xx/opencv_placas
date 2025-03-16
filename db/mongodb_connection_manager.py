from pymongo import MongoClient

class MongoDBConnectionManager:
    _client = None
    _db = None
    _db_name="db_placas"

    @classmethod
    def get_db(cls):
        if cls._client is None:
            cls._client = MongoClient("mongodb://localhost:27017/")        
        if cls._db is None:
            cls._db = cls._client[cls._db_name]
        
        return cls._db
