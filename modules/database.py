import requests

def search_product(item:str, condicion:str = "and items.saldo>0")-> str:
    url = "http://local.compumax.ec:8750/webservices/precios/cargar_productos.php"

    try:
        response = requests.post(
            url= url,
            data={
                "idproducto": item,
                "condicion": condicion
            }
        )
        
        # Si la respuesta tiene contenido
        if len(response.text) > 3:
            response = response.text
        else:
            response = "El código o el item no existe en la base de datos"

    except Exception as e:
        response = {
            "status": "Error",
            "error": e
        }
    
    return response

if __name__ == "__main__":
    salida = search_product("HP AIO")
    print(salida)
