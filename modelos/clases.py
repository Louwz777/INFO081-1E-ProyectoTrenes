## modulo donde se definen las clases a utilizar en el proyecto
## objetos seran guardados en .json, a excepcion de los pasajeros que sera en un .parquet

import json;
import os;
import pandas as pd;

##crea una variable con la ruta de la carpeta datos


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

    def __init__(self,creacion,id,inicio,destino,retorno):
        self.id = id
        self.creacion = creacion
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

    def __init__(self,nombre:str,poblacion:int,lineas:list,generador=None):
        self.nombre = nombre
        self.poblacion = poblacion
        self.lineas = lineas 
        self.generador = generador
        

    def convertir_dicc(self):
        return {
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "lineas": self.lineas
            }

"""
# Funciones para guardar objetos
"""


def guardar_objetos(datos: dict, ruta: str):
    
    """       
    ## funcion para guardar objetos en un .json
    ## POR FAVOR CAMBIEN LA RUTA DEL ARCHIVO SEGUN SU CLASE        
    """   
    
    ## Funcion para abrir el archivo, si existe carga su contenido, si no existe o si da error crea un diccionario vacio
    if os.path.exists(ruta):
        with open(ruta, 'r+', encoding='utf-8') as file:
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
    with open(ruta, 'w', encoding='utf-8') as file:
        json.dump(contenido, file, indent=4, ensure_ascii=False)
        
"""   
## Prueba guardar objetos
 
# tren1 = tren("lento", 125, 100, 50)
# dic_tren=tren1.convertir_dicc()
# guardar_objetos(dic_tren, "modelos/trenes.json")

"""



def guardar_pasajeros(datos: dict, ruta: str):
    
    dataframe = pd.DataFrame([datos])
    
    #Si el archivo no existe crea uno nuevo
    if (os.path.exists(ruta)==False):
        dataframe.to_parquet(ruta, index=False)
        return
    #si el archivo existe lo carga
    existente=pd.read_parquet(ruta)
    
    id=datos.get("id")
    
    #revisa si el diccionario recibido tiene id, si no lo tiene lanza un error
    if id is None:
        raise ValueError("El diccionario debe tener una clave id.")
    
    #copia el DataFrame existente sin el pasajero con el id recibido en un archivo temporal
    temp=existente[existente['id'] != id]
    
    #concatena el pasajero nuevo con los del archivo temporal y lo guarda
    actualizado=pd.concat([temp,dataframe], ignore_index=True)
    actualizado.to_parquet(ruta, index=False)

"""
Funciones para lectura de objetos
"""

def json_dicc(ruta: str):
    """
    recibe una ruta de archivo .json y devuelve su contenido como diccionario
    cambiar ruta segun su clase
    no se porque hice esta funcion si las siguiente funcione hace lo mismo
    """
    
    #Si no existe el archivo devuelve un diccionario vacio
    if (os.path.exists(ruta)==False):
        return {}
   
    #si existe abre y devuelve el contenido, si da error devuelve un diccionario vacio
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def cargar_objetos(archivo: str,clase) -> list:
    """
    devuelve una lista de objetos cargados desde un archivo .json
    """
    #abre el archivo y carga su contenido como diccionario
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    #lista que se va a retornar
    objetos = []
    
    #por cada 
    for atributos in data.values():
        objetos.append(clase(**atributos))

    return objetos


"""
##comprobar carga de objetos
trenes_cargados= cargar_trenes("modelos/trenes.json")
for i in dicc:
    print(f"Tren: {i}, Atributos: {dicc[i]}")
"""
