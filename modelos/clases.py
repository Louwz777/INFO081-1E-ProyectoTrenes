## modulo donde se definen las clases a utilizar en el proyecto
## objetos seran guardados en .json, a excepcion de los pasajeros que sera en un .parquet

class tren:
    ## ppv= pasajeros por vagon
    ## ccv= cantidad de vagones
    def __init__(self,nombre,velocidad,ppv,ccv):
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