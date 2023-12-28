try:
    from databases import FireStoreBase
except:
    import databases.FireStoreBase as FireStoreBase

# Iniciamos el objeto para Alarma
alarm = FireStoreBase.Firestore('alarm')

def get_alarm_status():
    resposne = alarm.get_value('alarm')

    if resposne:
        return resposne
    else: 
        return False
    
def update_alarm_status(status):
    data = {'alarm': status}
    response = alarm.update_create_registry(data)
    if response:
        return {"status": response}
    else:
        return {"status": False}

if __name__ == '__main__':
    print(get_alarm_status())
    print(update_alarm_status(False))