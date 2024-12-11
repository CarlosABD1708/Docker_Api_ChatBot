from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from pyswip import Prolog
from bot import sesiones,lock,manejar_interaccion

app = Flask(__name__)
CORS(app)  # Habilitar CORS para la API

# Conexión a la base de datos PostgreSQL
def obtener_conexion():
    return psycopg2.connect(
        dbname='mapun_database',
        user='admin_user',
        password='6sPFQ4BlUbe183EfcivR23N5lCeUePDf',
        host='dpg-ct2ltslsvqrc738cr960-a.oregon-postgres.render.com',
        port='5432'
    )

# Inicializar Prolog
prolog = Prolog()

# Cargar archivo Prolog
prolog.consult('conocimiento.pl')

def cargar_datos_en_prolog():
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Cargar facultades
    cursor.execute("SELECT nombre, descripcion, coordenadas FROM facultades")
    for nombre, descripcion, coordenadas in cursor.fetchall():
        if coordenadas:
            coord_lat, coord_long = map(float, coordenadas.strip('()').split(','))
        else:
            coord_lat, coord_long = 0.0, 0.0
        print(f'Cargando facultad: facultad("{nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
        prolog.assertz(f'facultad("{nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')

    # Cargar edificios
    cursor.execute("SELECT nombre, coordenadas, descripcion, facultad_id FROM edificios")
    for nombre, coordenadas, descripcion, facultad_id in cursor.fetchall():
        cursor.execute("SELECT nombre FROM facultades WHERE id = %s", (facultad_id,))
        facultad_result = cursor.fetchone()
        if facultad_result is not None:
            facultad_nombre = facultad_result[0]
        else:
            print(f"Advertencia: Facultad con ID {facultad_id} no encontrada. Se omitirá el edificio {nombre}.")
            continue

        if coordenadas:
            coord_lat, coord_long = map(float, coordenadas.strip('()').split(','))
        else:
            coord_lat, coord_long = 0.0, 0.0
        print(f'Cargando edificio: edificio("{nombre}", "{descripcion}", "{facultad_nombre}", ({coord_lat}, {coord_long}))')
        prolog.assertz(f'edificio("{nombre}", "{descripcion}", "{facultad_nombre}", ({coord_lat}, {coord_long}))')

    # Cargar oficinas
    cursor.execute("SELECT nombre, edificio_id, descripcion, coordenadas FROM oficinas")
    for nombre, edificio_id, descripcion, coordenadas in cursor.fetchall():
        cursor.execute("SELECT nombre FROM edificios WHERE id = %s", (edificio_id,))
        edificio_result = cursor.fetchone()
        if edificio_result is not None:
            edificio_nombre = edificio_result[0]
        else:
            print(f"Advertencia: Edificio con ID {edificio_id} no encontrado. Se omitirá la oficina {nombre}.")
            continue

        if coordenadas:
            coord_lat, coord_long = map(float, coordenadas.strip('()').split(','))
        else:
            coord_lat, coord_long = 0.0, 0.0
        print(f'Cargando oficina: oficina("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
        prolog.assertz(f'oficina("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')

    # Cargar aulas
    cursor.execute("SELECT nombre, edificio_id, descripcion, coordenadas FROM aulas")
    for nombre, edificio_id, descripcion, coordenadas in cursor.fetchall():
        cursor.execute("SELECT nombre FROM edificios WHERE id = %s", (edificio_id,))
        edificio_result = cursor.fetchone()
        if edificio_result is not None:
            edificio_nombre = edificio_result[0]
        else:
            print(f"Advertencia: Edificio con ID {edificio_id} no encontrado. Se omitirá el aula {nombre}.")
            continue

        if coordenadas:
            coord_lat, coord_long = map(float, coordenadas.strip('()').split(','))
        else:
            coord_lat, coord_long = 0.0, 0.0
        print(f'Cargando aula: aula("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
        prolog.assertz(f'aula("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
    # Cargar laboratorios
    cursor.execute("SELECT nombre, edificio_id, descripcion, coordenadas FROM laboratorios")
    for nombre, edificio_id, descripcion, coordenadas in cursor.fetchall():
        cursor.execute("SELECT nombre FROM edificios WHERE id = %s", (edificio_id,))
        edificio_result = cursor.fetchone()
        if edificio_result is not None:
            edificio_nombre = edificio_result[0]
        else:
            print(f"Advertencia: Edificio con ID {edificio_id} no encontrado. Se omitirá el aula {nombre}.")
            continue

        if coordenadas:
            coord_lat, coord_long = map(float, coordenadas.strip('()').split(','))
        else:
            coord_lat, coord_long = 0.0, 0.0
        print(f'Cargando laboratorio: laboratorio("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
        prolog.assertz(f'laboratorio("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')

    # Cargar lugares de interés
    cursor.execute("SELECT nombre, edificio_id, descripcion, coordenadas FROM lugares_interes")
    for nombre, edificio_id, descripcion, coordenadas in cursor.fetchall():
        cursor.execute("SELECT nombre FROM edificios WHERE id = %s", (edificio_id,))
        edificio_result = cursor.fetchone()
        if edificio_result is not None:
            edificio_nombre = edificio_result[0]
        else:
            print(f"Advertencia: Edificio con ID {edificio_id} no encontrado. Se omitirá el lugar de interés {nombre}.")
            continue

        if coordenadas:
            coord_lat, coord_long = map(float, coordenadas.strip('()').split(','))
        else:
            coord_lat, coord_long = 0.0, 0.0
        print(f'Cargando lugar de interés: lugar_interes("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
        prolog.assertz(f'lugar_interes("{nombre}", "{edificio_nombre}", "{descripcion}", ({coord_lat}, {coord_long}))')
 
    conn.close()

@app.route('/ubicacion_oficina', methods=['GET'])
def ubicacion_oficina():
    nombre_oficina = request.args.get('nombre')
    
    # Intentar consulta sin coordenadas primero
    query = f'oficina("{nombre_oficina}", Edificio, _, (Lat, Long))'
    print(f"Prolog Query: {query}")  # Registro para ver la consulta
    
    result = list(prolog.query(query))
    print(f"Prolog Result: {result}")  # Registro para ver el resultado de la consulta
    
    if result:
        # Si se encuentra la oficina, procesar coordenadas
        lat = result[0]['Lat']
        long = result[0]['Long']
        edificio = result[0]['Edificio'].decode('utf-8') if isinstance(result[0]['Edificio'], bytes) else result[0]['Edificio']
        
        # Devuelve el resultado en formato JSON
        return jsonify({"edificio": edificio, "coordenadas": {'lat': lat, 'long': long}})
    
    # Si no se encuentra la oficina
    return jsonify({"error": f"Oficina '{nombre_oficina}' no encontrada"}), 404

@app.route('/ubicacion_aula', methods=['GET'])
def ubicacion_aula():
    nombre_aula = request.args.get('nombre')
    query = f'aula("{nombre_aula}", Edificio, _)'
    print(f"Prolog Query: {query}")  # Registro para ver la consulta
    result = list(prolog.query(query))
    print(f"Prolog Result: {result}")  # Registro para ver el resultado de la consulta
    if result:
        edificio = result[0]['Edificio'].decode('utf-8') if isinstance(result[0]['Edificio'], bytes) else result[0]['Edificio']
        return jsonify({"edificio": edificio})
    return jsonify({"error": f"Aula '{nombre_aula}' no encontrada"}), 404

@app.route('/ubicacion_lugar', methods=['GET'])
def ubicacion_lugar():
    nombre_lugar = request.args.get('nombre')
    query = f'lugar_interes("{nombre_lugar}", Edificio, _)'
    print(f"Prolog Query: {query}")  # Registro para ver la consulta
    result = list(prolog.query(query))
    print(f"Prolog Result: {result}")  # Registro para ver el resultado de la consulta
    if result:
        edificio = result[0]['Edificio'].decode('utf-8') if isinstance(result[0]['Edificio'], bytes) else result[0]['Edificio']
        return jsonify({"edificio": edificio})
    return jsonify({"error": f"Lugar de interés '{nombre_lugar}' no encontrado"}), 404

@app.route('/facultad_de_edificio', methods=['GET'])
def facultad_de_edificio():
    nombre_edificio = request.args.get('nombre')
    query = f'facultad_de_edificio("{nombre_edificio}", Facultad)'
    print(f"Prolog Query: {query}")  # Registro para ver la consulta
    result = list(prolog.query(query))
    print(f"Prolog Result: {result}")  # Registro para ver el resultado de la consulta
    if result:
        facultad = result[0]['Facultad'].decode('utf-8') if isinstance(result[0]['Facultad'], bytes) else result[0]['Facultad']
        return jsonify({"facultad": facultad})
    return jsonify({"error": f"Edificio '{nombre_edificio}' no encontrado"}), 404

@app.route('/coordenadas_edificio', methods=['GET']) 
def coordenadas_edificio():
    nombre_edificio = request.args.get('nombre')
    query = f'coordenadas_edificio("{nombre_edificio}", (Lat, Long))'
    print(f"Prolog Query: {query}")  # Registro para ver la consulta
    result = list(prolog.query(query))
    print(f"Prolog Result: {result}")  # Registro para ver el resultado de la consulta
    if result:
        lat = result[0]['Lat']
        long = result[0]['Long']
        return jsonify({"coordenadas": {"lat": lat, "long": long}})
    return jsonify({"error": f"Edificio '{nombre_edificio}' no encontrado"}), 404


@app.route('/buscar_lugar', methods=['POST'])
def buscar_lugar():
    # Obtener parámetros de la solicitud
    session_id = request.json.get("session_id")
    nombre_lugar = request.json.get('nombre')
    
    if not nombre_lugar:
        return jsonify({"error": "El parámetro 'nombre' es obligatorio"}), 400
    if not session_id:
        return jsonify({"error": "El parámetro 'session_id' es obligatorio"}), 400

    try:
        # Realizar la consulta para buscar el tipo de lugar
        resultados_tipo = list(prolog.query(f'buscar_lugar("{nombre_lugar}", Tipo)'))
        
        if not resultados_tipo:
            return jsonify({"error": "Lugar no encontrado"}), 404
        
        tipo = resultados_tipo[0]["Tipo"]

        # Construir la consulta para obtener las coordenadas
        regla_coordenadas = f'coordenadas_{tipo}("{nombre_lugar}", (Lat, Long))'
        resultados_coordenadas = list(prolog.query(regla_coordenadas))
        
        if not resultados_coordenadas:
            return jsonify({
                "nombre": nombre_lugar,
                "tipo": tipo,
                "error": "Coordenadas no encontradas"
            }), 404

        # Extraer coordenadas
        coordenadas = resultados_coordenadas[0]
        lat, lon = coordenadas["Lat"], coordenadas["Long"]

        # Devolver el resultado como JSON
        return jsonify({
            "nombre": nombre_lugar,
            "tipo": tipo,
            "coordenadas": {
                "latitud": lat,
                "longitud": lon
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para iniciar una sesión
@app.route('/iniciar', methods=['POST'])
def iniciar_sesion():
    session_id = request.json.get("session_id")
    if not session_id:
        return jsonify({"error": "Se requiere un session_id"}), 400
    
    with lock:
        if session_id in sesiones:
            return jsonify({"message": "Sesión ya iniciada", "session_id": session_id})
        sesiones[session_id] = []
    return jsonify({"message": "Sesión iniciada", "session_id": session_id})

# Ruta para enviar un mensaje
@app.route('/mensaje', methods=['POST'])
def procesar_mensaje():
    session_id = request.json.get("session_id")
    mensaje = request.json.get("mensaje")
    
    if not session_id or not mensaje:
        return jsonify({"error": "Se requiere session_id y mensaje"}), 400
    
    with lock:
        if session_id not in sesiones:
            return jsonify({"error": "Sesión no encontrada"}), 404
    
    # Procesar el mensaje en un hilo
    respuesta = manejar_interaccion(session_id, mensaje)
    sesiones[session_id].append({"mensaje": mensaje, "respuesta": respuesta})
    return jsonify(respuesta)

# Ruta para finalizar una sesión
@app.route('/finalizar', methods=['POST'])
def finalizar_sesion():
    session_id = request.json.get("session_id")
    if not session_id:
        return jsonify({"error": "Se requiere session_id"}), 400
    
    with lock:
        if session_id in sesiones:
            del sesiones[session_id]
            return jsonify({"message": "Sesión finalizada"})
        else:
            return jsonify({"error": "Sesión no encontrada"}), 404

if __name__ == '__main__':
    cargar_datos_en_prolog()  # Cargar datos al iniciar la API
    app.run()
