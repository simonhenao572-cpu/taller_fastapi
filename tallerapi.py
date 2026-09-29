### 2. Archivo Python (`taller_videojuegos.py`)
"""
==========================================================================
 TALLER PARA LA CASA — FastAPI + MongoDB (async)[cite: 3]
 Ficha 3468252 (ADSO - SENA)
==========================================================================

 Tema: una API para un CATALOGO DE VIDEOJUEGOS, guardado en MongoDB Atlas[cite: 3].

 Idea del taller: Aplicar el patron de conexion asincrona a un tema nuevo[cite: 3].
 No copies: vuelve a pensarlo[cite: 3].

 Objetivo: que los datos PERDUREN[cite: 3]. Al terminar, crea un videojuego,
 reinicia el servidor y comprueba que sigue ahi[cite: 3].

 Como trabajar:
   1. Activa tu entorno virtual[cite: 3].
   2. Instala (si no lo tienes):   pip install "fastapi[standard]" "pymongo[srv]"[cite: 3]
   3. Reemplaza <password> por tu clave real de Atlas[cite: 3].
   4. Corre el servidor:           uvicorn taller_videojuegos:app --reload
   5. Abre en el navegador:        http://127.0.0.1:8000/docs[cite: 3]
   6. Completa cada # TODO y pruebalo desde /docs con "Try it out"[cite: 3].

 Recuerda las 3 reglas de esta clase:
   - async def  en cada endpoint[cite: 3].
   - await      antes de cada operacion de base de datos[cite: 3].
   - str(_id)   para convertir el ObjectId a texto antes de devolverlo[cite: 3].
==========================================================================
"""

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from bson import ObjectId
from pydantic import BaseModel

app = FastAPI()

# --------------------------------------------------------------------------
#  CONEXION  (ya esta lista - solo cambia tu <password>)[cite: 3]
#  Usamos una base y coleccion nuevas para este taller[cite: 3].
# --------------------------------------------------------------------------
URI = "mongodb+srv://admin_sena:hola123@cluster0.2zhh6i9.mongodb.net/" #[cite: 3]
cliente = AsyncMongoClient(URI)
db = cliente["sena_adso_db"]
videojuegos = db["videojuegos"]

# Molde de validacion para crear videojuegos[cite: 3]
class Videojuego(BaseModel):
    titulo: str
    consola: str
    precio: float


# ==========================================================================
#  YA RESUELTO — Listar todos          (GET /videojuegos)
#  Te lo dejamos hecho como ejemplo del patron asincrono + el _id[cite: 3].
# ==========================================================================
@app.get("/videojuegos")
async def listar():
    resultado = []
    async for v in videojuegos.find():
        v["_id"] = str(v["_id"])       # ObjectId -> texto (para JSON)[cite: 3]
        resultado.append(v)
    return resultado


# ==========================================================================
#  EJERCICIO 1 — Crear un videojuego    (POST /videojuegos)
#  Objetivo: recibir un Videojuego validado y GUARDARLO en Atlas[cite: 3].
#  Pistas:   la funcion recibe  nuevo: Videojuego[cite: 3]
#            usa  await videojuegos.insert_one(nuevo.model_dump())[cite: 3]
#            devuelve el id nuevo como texto:  str(r.inserted_id)[cite: 3]
# ==========================================================================
# TODO (EJ. 1): escribe aqui el endpoint POST "/videojuegos"[cite: 3]
@app.post("/videojuegos")
async def crear(nuevo: Videojuego):
    r = await videojuegos.insert_one(nuevo.model_dump())
    return {"_id": str(r.inserted_id), **nuevo.model_dump()}


# ==========================================================================
#  EJERCICIO 2 — Un videojuego por id   (GET /videojuegos/{id})
#  Objetivo: /videojuegos/{id} devuelve SOLO ese videojuego[cite: 3].
#  Pistas:   el id es un texto largo -> recibelo como  id: str[cite: 3]
#            busca con  await videojuegos.find_one({"_id": ObjectId(id)})[cite: 3]
#            si es None -> {"error": "No encontrado"}[cite: 3]
#            si existe  -> convierte su _id a texto y devuelvelo[cite: 3]
# ==========================================================================
# TODO (EJ. 2): escribe aqui el endpoint GET "/videojuegos/{id}"[cite: 3]
@app.get("/videojuegos/{id}")
async def obtener(id: str):
    if not ObjectId.is_valid(id):
        return {"error": "No encontrado"}
    v = await videojuegos.find_one({"_id": ObjectId(id)})
    if v is None:
        return {"error": "No encontrado"}
    v["_id"] = str(v["_id"])
    return v


# ==========================================================================
#  EJERCICIO 3 — Actualizar un juego    (PUT /videojuegos/{id})
#  Objetivo: cambiar titulo, consola y precio de un juego por su id[cite: 3].
#  Pistas:   await videojuegos.update_one(
#                {"_id": ObjectId(id)}, {"$set": datos.model_dump()})[cite: 3]
#            revisa  r.matched_count == 0  para el caso "no encontrado"[cite: 3]
# ==========================================================================
# TODO (EJ. 3): escribe aqui el endpoint PUT "/videojuegos/{id}"[cite: 3]
@app.put("/videojuegos/{id}")
async def actualizar(id: str, datos: Videojuego):
    if not ObjectId.is_valid(id):
        return {"error": "No encontrado"}
    r = await videojuegos.update_one(
        {"_id": ObjectId(id)}, {"$set": datos.model_dump()})
    if r.matched_count == 0:
        return {"error": "No encontrado"}
    return {"mensaje": "Actualizado", "_id": id, **datos.model_dump()}


# ==========================================================================
#  EJERCICIO 4 — Eliminar un juego      (DELETE /videojuegos/{id})
#  Objetivo: borrar un videojuego por su id[cite: 3].
#  Pistas:   await videojuegos.delete_one({"_id": ObjectId(id)})[cite: 3]
#            revisa  r.deleted_count == 0  para el caso "no encontrado"[cite: 3]
# ==========================================================================
# TODO (EJ. 4): escribe aqui el endpoint DELETE "/videojuegos/{id}"[cite: 3]
@app.delete("/videojuegos/{id}")
async def eliminar(id: str):
    if not ObjectId.is_valid(id):
        return {"error": "No encontrado"}
    r = await videojuegos.delete_one({"_id": ObjectId(id)})
    if r.deleted_count == 0:
        return {"error": "No encontrado"}
    return {"mensaje": "Eliminado"}


# ==========================================================================
#  RETO (para nota maxima) — Filtro por consola
#  Objetivo: /buscar?consola=PC devuelve los juegos de esa plataforma[cite: 3].
#  Pistas:   parametro de consulta  consola: str = ""[cite: 3]
#            recorre con async for  videojuegos.find({"consola": consola})[cite: 3]
#            no olvides convertir el _id de cada uno a texto[cite: 3]
# ==========================================================================
# TODO (reto): escribe aqui el endpoint GET "/buscar"[cite: 3]
@app.get("/buscar")
async def buscar(consola: str = ""):
    resultado = []
    async for v in videojuegos.find({"consola": consola}):
        v["_id"] = str(v["_id"])
        resultado.append(v)
    return resultado


# --------------------------------------------------------------------------
#  La prueba final (persistencia): crea un juego con POST, apaga el
#  servidor (Ctrl+C), enciendelo de nuevo y llama GET /videojuegos[cite: 3].
#  Si el juego SIGUE ahi, lograste el objetivo de la clase[cite: 3].
#
#  Nota: POST, PUT y DELETE se prueban desde /docs, no desde la barra
#  del navegador (esa solo hace GET)[cite: 3].
# --------------------------------------------------------------------------