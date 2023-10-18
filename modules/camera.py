import cv2, os, imutils
import numpy as np

dataPath = "./facesData"
fileFacesXML = "./facesData/haarcascade_frontalface_default.xml"
print(fileFacesXML)

# Capturamos los rostros de las personas
def capture(name:str):
    """
    :name -> Nombre de la persona
    :fileName -> Usarlo cuando se requiera usar un video como fuente

    Función para detectar rostros y guardarlos para luego entrenar un modelo
    """
    personPath = f"{dataPath}/{name}"
    
    if not os.path.exists(personPath):
        print(f"Carpeta creada: {personPath}")
        os.makedirs(personPath)
    
    # Configuramos en caso de que la entrada sea un video
    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(f"{fileFacesXML}")
    count = 0 

    while True:
        ret, frame = cap.read()
        if ret == False: break
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            rostro = auxFrame[x:y+h,x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(f"{personPath}/rostro_{count}.jpg", rostro)
            count = count + 1
        cv2.imshow("frame", frame)

        k = cv2.waitKey(1)
        if k == 27 or count >= 300:
            break
    
    cap.release()
    cv2.destroyAllWindows()

def find():
    """
    Activamos el modulo de la camara en vivo, se detiene cuando 
    detecta un rostro y devuelve true
    """
    cap = cv2.VideoCapture(0)
    faceClassif = cv2.CascadeClassifier(fileFacesXML)

    while True:
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)
        if type(faces) != tuple:
            return True

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # capture("Jorge", "none")
    salida = find()
    print(salida)
