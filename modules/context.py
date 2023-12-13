# Nombre del Robot
nombre = "Maxi"

def read_file(ruta:str)->str:
    # Esta ruta apunta al directorio principal
    ruta = 'context/' + ruta

    with open(ruta, 'r') as archivo:
        contenido = archivo.read()
    return contenido

entender_consulta = read_file('entender_consulta.txt')

context = read_file('context.txt')
context = context.replace('{nombre}', nombre)

caracteristicas_producto = read_file('caracteristicas_producto.txt')

no_producto = read_file('no_producto.txt')

error_mensaje = read_file('error_mensaje.txt')
