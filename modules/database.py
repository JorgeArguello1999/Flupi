import requests
import json

# URL de la API donde esta la base de datos
url = "http://local.compumax.ec:8750/webservices/precios/cargar_productos.php"

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

        # Si la respuesta tiene contenido
        if data:
            return data
        else:
            return "El código o el item no existe en la base de datos"
        
    except Exception as e:
        response = {
            "status": "Error",
            "error": e
        }

        return response

if __name__ == "__main__":
    salida = search_product("laptop")
    print(salida)
