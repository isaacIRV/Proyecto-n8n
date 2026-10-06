import json
import os
import sys
from pymongo import MongoClient

# Configurar la salida estándar en UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

uri = "mongodb://user_n8n:clave123@ac-yu6ks6r-shard-00-00.lzzriyu.mongodb.net:27017,ac-yu6ks6r-shard-00-01.lzzriyu.mongodb.net:27017,ac-yu6ks6r-shard-00-02.lzzriyu.mongodb.net:27017/bdmongo?ssl=true&replicaSet=atlas-q01cz0-shard-0&authSource=admin"

try:
    archivo = "datos_ventas.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client["bdmongo"]
        collection = db["cierre_diario_ventas"]

        if isinstance(datos, list):
            res = collection.insert_many(datos)
            print(f"EXITO: Se insertaron {len(res.inserted_ids)} registros en bdmongo.", flush=True)
        else:
            res = collection.insert_one(datos)
            print(f"EXITO: Registro insertado con ID {res.inserted_id}", flush=True)
    else:
        print(f"ERROR: No se encontro el archivo {archivo}", flush=True)
except Exception as e:
    print(f"ERROR: {e}", flush=True)