try:
    from databases import firestore
except:
    import firestore

# Iniciamos el objeto para contextos
alarm = firestore.Firestore()

def get_alarm_status():
    resposne = alarm.get_value('contextos', 'alarm')

    if resposne:
        return resposne
    else: 
        return False
    
def update_alarm_status(status):
    data = {'alarm': status}
    response = alarm.update_create_registry('contextos', data)
    if response:
        return {"status": response}
    else:
        return {"status": False}

if __name__ == '__main__':
    print(get_alarm_status())
    print(update_alarm_status(False))