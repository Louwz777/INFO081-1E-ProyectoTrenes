## modulo donde se definen las clases a utilizar en el proyecto
## objetos seran guardados en .json, a excepcion de los pasajeros que sera en un .parquet

import json;
import os;

class tren:
    ## ppv= pasajeros por vagon
    ## ccv= cantidad de vagones
    def __init__(self,nombre:str,velocidad:int,ppv:int,ccv:int):
        self.nombre = nombre
        self.velocidad = velocidad
        self.ppv = ppv
        self.ccv = ccv
    
    def capacidad(self):
        return self.ccv*self.ppv
    def convertir_dicc(self):
        return {
            "nombre": self.nombre,
            "velocidad": self.velocidad,
            "ppv": self.ppv,
            "ccv": self.ccv
            }
    
class pasajero:

    def __init__(self,id,inicio,destino,retorno):
        self.id = id
        self.inicio = inicio
        self.destino = destino
        self.retorno = retorno

    def convertir_dicc(self):
        return {
            "id": self.id,
            "inicio": self.inicio,
            "destino": self.destino,
            "retorno": self.retorno
            }
class estacion:

    def __init__(self,nombre:str,poblacion:int,lineas:list):
        self.nombre = nombre
        self.poblacion = poblacion
        self.lineas = lineas 

    def convertir_dicc(self):
        return {
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "lineas": self.lineas
            }
        
## funcion para guardar objetos en un .json
## POR FAVOR CAMBIEN LA RUTA DEL ARCHIVO SEGUN SU CLASE        
        
def guardar_objetos(datos: dict, archivo: str):

    
    ## Funcion para abrir el archivo, si existe carga su contenido, si no existe o si da error crea un diccionario vacio
    if os.path.exists(archivo):
        with open(archivo, 'r+', encoding='utf-8') as file:
            try:
                contenido = json.load(file)
            except json.JSONDecodeError:
                contenido = {}
    else:
        contenido = {}
    
    
    ## la una clave que si o si debe estar en el diccionario es "nombre
    ## Es necesaria para identificar el objeto y evitar duplicados (si ya exite uno con el mismo nombre se sobreescribe)
    nombre = datos.get("nombre")
    if nombre is None:
        raise ValueError("El diccionario debe tener una clave nombre.")
    contenido[nombre] = datos
    
    ## guarda el contenido actualizado en el archivo
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)
        
        
# tren1 = tren("lento", 125, 100, 50)
# dic_tren=tren1.convertir_dicc()
# guardar_objetos(dic_tren, "modelos/trenes.json")
