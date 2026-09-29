# Taller para la casa — FastAPI + MongoDB (async)

**Ficha 3468252 (ADSO — SENA)**

Vas a construir una API para un **catálogo de videojuegos**, guardada de verdad en MongoDB Atlas. Es la misma idea que trabajamos en clase, pero al aplicar el patrón a un tema nuevo es como de verdad se afianza el conocimiento. Trabaja sobre el archivo `taller_videojuegos.py` y completa cada `# TODO`.

**Objetivo de la clase:** que los datos **perduren**. Al final, crea un videojuego, reinicia el servidor y comprueba que sigue ahí.

---

## Cómo ponerlo a correr

```bash
# 1. Activa tu entorno virtual
python -m venv venv
source venv/bin/activate        # En Windows:  venv\Scripts\activate

# 2. Instala lo necesario (si no lo tienes ya)
pip install "fastapi[standard]" "pymongo[srv]"

# 3. Abre taller_videojuegos.py y reemplaza <password> por tu clave real de Atlas

# 4. Arranca el servidor
uvicorn taller_videojuegos:app --reload

# 5. Abre en el navegador
#    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


#Las 3 reglas de esta clase: 
# 1. async def en cada endpoint.  
# 2. await antes de cada operación de base de datos (si lo #olvidas, falla en silencio).  
# 3. str(_id) para convertir el ObjectId a texto antes de devolverlo (si no, FastAPI se cae).  

#,Endpoint,Operación,Cómo probarlo
—,GET /videojuegos,Listar todos,ya resuelto (referencia)[cite: 2]
1,POST /videojuegos,Crear (insert_one),"/docs → ""Try it out""[cite: 2]"
2,GET /videojuegos/{id},Uno por id (find_one + ObjectId),copia un _id de la lista[cite: 2]
3,PUT /videojuegos/{id},Actualizar (update_one + $set),/docs[cite: 2]
4,DELETE /videojuegos/{id},Eliminar (delete_one),/docs[cite: 2]