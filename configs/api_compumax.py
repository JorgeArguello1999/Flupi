import requests
import json
import os 

# URL de la API donde esta la base de datos
url = os.environ.get("API_ROUTE")

def html_tabla(data:str):
    if data:
        # Encabezados de la tabla
        encabezados = '<table border="1" width="90%"><tr><th>ID</th><th>Nombre</th><th>Precio</th></tr>' 

        # Contenido de la tabla
        contenido_tabla = ""
        for items in data:
            fila = f"<tr><td>{items['iditem']}</td><td>{items['nitem']}</td><td>${items['saldo']}</td></tr>"
            contenido_tabla += fila

        # Cierre de la tabla
        cierre_tabla = "</table>"

        # Combinar todos los elementos para formar la tabla completa
        tabla_html = f"{encabezados}\n{contenido_tabla}\n{cierre_tabla}"
        return tabla_html
    else:
        return False

def search_product(item:str, condicion:str = "and items.saldo>0")-> str:
    """
    :param item el id o el nombre del item
    :condicion "" por defecto -> "and items.saldo>0" 
    """
    try:
        response = requests.post(
            url= url,
            data={
                "idproducto": item,
                "condicion": condicion
            }
        )

        data = response.content
        data = data.decode("utf-8")
        data = json.loads(data)

        return html_tabla(data)
        
    except Exception as e:
        response = {
            "status": "Error",
            "error": e
        }

        return response

if __name__ == "__main__":
    salida = search_product("laptop")
    print(salida)
