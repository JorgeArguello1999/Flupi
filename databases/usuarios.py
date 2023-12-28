from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import uuid

import FireStoreUsuarios

# Iniciamos el objeto para contextos
usuarios = FireStoreUsuarios.Users()

def create_user(username:str, password:str) -> bool:
    token = str(uuid.uuid4())
    hashed_password = generate_password_hash(password)

    data = {
        "username": username,
        "password": hashed_password,
        "token": token
    }

    return usuarios.create_user(data)

def get_all_users() -> list:
    response = usuarios.get_users()
    data = [list(i.values()) for i in response.values()]
    return data

def search_user(user:str, password:str) -> bool:
    response = usuarios.get_users()

    data = [ i for i in response.values() if i['username'] == user]
    if data:
        data = data[0]
        if check_password_hash(data['password'], password):
            return True

    else:
        return False

def search_token(token:str) -> bool:
    response = usuarios.get_users()

    data = [ i for i in response.values() if i['token'] == token]
    if data:
        return True
    else:
        return False
    
def get_user_by_username(user:str) -> bool:
    response = usuarios.get_users()

    data = [ i for i in response.values() if i['username'] == user] 
    if data:
        return True
    else: 
        return False

def delete_user_by_id(user_id) -> bool:
    if usuarios.delete_user(user_id):
        return True
    else:
        return False
  
if __name__ == '__main__':
    print(get_all_users())
    # print(create_user("jorge", "hola"))
    # print(search_user(user='jorge', password='hola'))
    # print(get_user_by_username('jorge'))
    print(delete_user_by_id('jorge'))