try:
    from databases import FireStoreBase
except:
    import FireStoreBase

# Iniciamos el objeto para IPS
home = FireStoreBase.Firestore('home')

def get_home() -> str:
    return home.get_value('home')

def update_home(data:str) -> bool:
    try:
        data = {'home': data}
        return home.update_create_registry(data)
    except Exception as e:
        return False

if __name__ == '__main__':
    print(get_home())
    print(update_home("<h1> Hola </h1>"))
