import requests
import json
import os 

# URL de la API donde esta la base de datos
url = os.environ.get("API_ROUTE")

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
            return [{key: item[key] for key in ['iditem', 'nitem', 'pventa']} for item in data]
        else:
            return False
        
    except Exception as e:
        response = {
            "status": "Error",
            "error": e
        }

        return response

if __name__ == "__main__":
    salida = search_product("laptop")
    print(salida)
