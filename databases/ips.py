try:
    from databases import FireStoreBase
except:
    import FireStoreBase

# Iniciamos el objeto para IPS
ips = FireStoreBase.Firestore('ips')

def get_ips() -> list:
    return ips.get_all().get('ips')

if __name__ == '__main__':
    print(get_ips()+["127.0.0.1"])