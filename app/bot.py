from flask import Flask, request, jsonify
from fuzzywuzzy import process
import re
import threading


# Diccionario de sinónimos
sinonimos = {
    "salon": "Aula",
    "Salon": "Aula",
    "Lab": "Laboratorio",
    "lab": "Laboratorio",
    "laboratorio": "Laboratorio",
    "Baño": "Baños",
    "baño": "Baños",
    "baños": "Baños"
}

# Lista de palabras clave específicas para la segunda verificación
palabras_clave = ["baños", "mujer", "hombre", "Mujer", "Hombre", "Hombres", "Mujeres"]

# Lista de palabras comunes de preguntas o consultas
palabras_de_pregunta = ["donde", "puedo", "encontrar", "como", "que", "cuando", "por", "para", "cuál", "de", "el", "la", "los", "las", "es", "esta", "está", "quién", "cuántos", "quiénes"]

# Almacén de sesiones activas
sesiones = {}
lock = threading.Lock()

# Función para cargar el archivo JSON
def cargar_lugares():
    lugares = {
        "lugares": [
        {
            "nombre": "Apoyo a la Docencia"
        },
        {
            "nombre": "Sala Polivalente"
        },
        {
            "nombre": "Modulo de Informacion Digital"
        },
        {
            "nombre": "Coordinacion de Unidad de Apoyo a la Docencia e Investigacion"
        },
        {
            "nombre": "Coordinacion de Sistemas y Difusion"
        },
        {
            "nombre": "Coordinacion de Laboratorios"
        },
        {
            "nombre": "Sala de Tutorias Y Asesorias"
        },
        {
            "nombre": "Area Tecnica 2 de Vinculacion y Proyectos Estrategicos"
        },
        {
            "nombre": "Bodega 5"
        },
        {
            "nombre": "Coordinacion de Vinculacion Y Proyectos Estrategicos"
        },
        {
            "nombre": "Bodega 4"
        },
        {
            "nombre": "Coordinacion de Servicio Social"
        },
        {
            "nombre": "Encargado de Plataformas Virtuales y Base de Datos"
        },
        {
            "nombre": "Bodega 2"
        },
        {
            "nombre": "Coordinacion de Investigacion y Posgrado"
        },
        {
            "nombre": "Bodega 3"
        },
        {
            "nombre": "Coordinacion de Turno"
        },
        {
            "nombre": "Area Tecnica 1 de Vinculacion y Proyectos Estrategicos"
        },
        {
            "nombre": "Coordinacion de Centros De Computo Y Red Informatica"
        },
        {
            "nombre": "Direccion"
        },
        {
            "nombre": "Coordinacion de Servicios Escolares"
        },
        {
            "nombre": "Coordinacion de Servicios Estudiantiles"
        },
        {
            "nombre": "Laboratorio 1"
        },
        {
            "nombre": "Laboratorio 2"
        },
        {
            "nombre": "Laboratorio 3"
        },
        {
            "nombre": "Area Balanzas"
        },
        {
            "nombre": "Area de Pruebas Mecanicas"
        },
        {
            "nombre": "Baños de Hombre B4"
        },
        {
            "nombre": "Baños de Hombre B2"
        },
        {
            "nombre": "Baños de Hombre B5"
        },
        {
            "nombre": "Baños de Hombre B6"
        },
        {
            "nombre": "Baños de Mujer B2"
        },
        {
            "nombre": "Baños de Mujer B4"
        },
        {
            "nombre": "Baños de Mujer B5"
        },
        {
            "nombre": "Baños de Mujer B6"
        },
        {
            "nombre": "Rampa Para Discapacitados"
        },
        {
            "nombre": "Aula 13"
        },
        {
            "nombre": "Aula 21"
        },
        {
            "nombre": "Aula 22"
        },
        {
            "nombre": "Sala Polivalente"
        },
        {
            "nombre": "Aula 8"
        },
        {
            "nombre": "Aula 15"
        },
        {
            "nombre": "Aula 3"
        },
        {
            "nombre": "Aula 16"
        },
        {
            "nombre": "Aula 17"
        },
        {
            "nombre": "Aula 6"
        },
        {
            "nombre": "Aula 18"
        },
        {
            "nombre": "Aula 20"
        },
        {
            "nombre": "CC3"
        },
        {
            "nombre": "Aula 2"
        },
        {
            "nombre": "Aula 1"
        },
        {
            "nombre": "Aula 14"
        },
        {
            "nombre": "Aula 4"
        },
        {
            "nombre": "CC5"
        },
        {
            "nombre": "CC4"
        },
        {
            "nombre": "CC2"
        },
        {
            "nombre": "CC1"
        },
        {
            "nombre": "Aula 19"
        },
        {
            "nombre": "Aula 12"
        },
        {
            "nombre": "Aula 10"
        },
        {
            "nombre": "Aula 9"
        },
        {
            "nombre": "Aula 11"
        },
        {
            "nombre": "Aula 5"
        },
        {
            "nombre": "Mapoteca"
        },
        {
            "nombre": "Sala De Usos Multiples"
        },
        {
            "nombre": "Posgrado 1"
        },
        {
            "nombre": "Posgrado 2"
        },
        {
            "nombre": "Aula 7"
        },
        {
            "nombre": "Facultad De Ingenieria Mochis"
        },
        {
            "nombre": "Unidad Academica De Negocios"
        },
        {
            "nombre": "Facultad De Ciencias De La Educacion"
        },
        {
            "nombre": "Facultad De Enfermeria Mochis"
        },
        {
            "nombre": "Facultad De Trabajo Social Mochis"
        },
        {
            "nombre": "Facultad De Medicina Culiacan - Extension Mochis"
        },
        {
            "nombre": "Unidad Academica De Derecho Y Ciencia Politica Los Mochis"
        },
        {
            "nombre": "Unidad Regional Norte"
        },
        {
            "nombre": "B1"
        },
        {
            "nombre": "B2"
        },
        {
            "nombre": "B3"
        },
        {
            "nombre": "B4"
        },
        {
            "nombre": "B5"
        },
        {
            "nombre": "Torre Academica"
        },
        {
            "nombre": "Vicerrectoria Unidad Regional Norte"
        },
        {
            "nombre": "Unidad Regional Norte"
        },
        {
            "nombre": "B6"
        },
        {
            "nombre": "B7"
        },
        {
            "nombre": "Geomatica"
        },
        {
            "nombre": "Diagnostico y Metrologia"
        },
        {
            "nombre": "Fotogrametria"
        },
        {
            "nombre": "Cartografia y S.I.G"
        },
        {
            "nombre": "Materiales Sustentables"
        },
        {
            "nombre": "Geotecnica"
        },
        {
            "nombre": "Mecanica de Materiales"
        },
        {
            "nombre": "Geologia"
        },
        {
            "nombre": "Construccion"
        },
        {
            "nombre": "Hidraulica"
        },
        {
            "nombre": "Potabilizacion de Aguas"
        },
        {
            "nombre": "Fisica Y Quimica"
        },
        {
            "nombre": "Quimica y Ambiental"
        },
        {
            "nombre": "Corrosion y Optica"
        },
        {
            "nombre": "Director"
        },
        {
            "nombre": "Secretaria Academica"
        },
        {
            "nombre": "Secretaria Administrativa"
        },
        {
            "nombre": "Coordinaciones de Carreras"
        },
        {
            "nombre": "Contabilidad"
        },
        {
            "nombre": "Secretaria"
        },
        {
            "nombre": "Sala de Directores"
        },
        {
            "nombre": "Bodega 1"
        }
        ]
    }
    return lugares["lugares"]

# Función para limpiar la frase de palabras no relevantes
def limpiar_frase(nombre_usuario):
    nombre_usuario = nombre_usuario.lower()
    palabras_limpias = [palabra for palabra in nombre_usuario.split() if palabra not in palabras_de_pregunta]
    return ' '.join(palabras_limpias)

# Función para buscar lugares de forma difusa
def buscar_lugar_approx(nombre_usuario, lista_lugares):
    for sinonimo, reemplazo in sinonimos.items():
        nombre_usuario = re.sub(r'\b' + re.escape(sinonimo) + r'\b', reemplazo, nombre_usuario, flags=re.IGNORECASE)

    nombres_lugares = [lugar["nombre"] for lugar in lista_lugares]
    resultados = process.extract(nombre_usuario, nombres_lugares, limit=5)
    return [(lugar, score) for lugar, score in resultados if score > 80]

# Función para filtrar los resultados según las palabras clave de género
def filtrar_por_genero(resultados, genero):
    return [(lugar, score) for lugar, score in resultados if genero.lower() in lugar.lower()]

# Función para manejar la conversación de un usuario
def manejar_interaccion(session_id, mensaje):
    lugares = cargar_lugares()
    mensaje_limpio = limpiar_frase(mensaje)
    
    # Revisar palabras clave de género
    if any(palabra in mensaje.lower() for palabra in ["mujer", "mujeres"]):
        genero = "mujer"
        resultados = buscar_lugar_approx(mensaje_limpio, lugares)
        resultados_filtrados = filtrar_por_genero(resultados, genero)
        return {"resultados": resultados_filtrados, "genero": genero}
    elif any(palabra in mensaje.lower() for palabra in ["hombre", "hombres"]):
        genero = "hombre"
        resultados = buscar_lugar_approx(mensaje_limpio, lugares)
        resultados_filtrados = filtrar_por_genero(resultados, genero)
        return {"resultados": resultados_filtrados, "genero": genero}
    else:
        resultados = buscar_lugar_approx(mensaje_limpio, lugares)
        return {"resultados": resultados, "genero": None}

