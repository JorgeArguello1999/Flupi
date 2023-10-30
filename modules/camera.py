import cv2, os, imutils, time
import numpy as np

dataPath = "./facesData"
fileFacesXML = "./haarcascade_frontalface_default.xml"

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
        try:
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
        except Exception as error:
            print("Colocate en el cuadro de la Imagen")
        
    cap.release()
    cv2.destroyAllWindows()

def fit():
    """
    Entrenamos el modelo con los rostros obtenidos
    """
    peopleList = os.listdir(dataPath)
    print('Lista de personas: ', peopleList)

    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir
        print('Leyendo las imágenes')

        for fileName in os.listdir(personPath):
            print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName,0))
            #image = cv2.imread(personPath+'/'+fileName,0)
            #cv2.imshow('image',image)
            #cv2.waitKey(10)
        label = label + 1

    # Métodos para entrenar el reconocedor
    face_recognizer = cv2.face.FisherFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))

    # Almacenando el modelo obtenido
    face_recognizer.write('modeloFisherFace.xml')
    print("Modelo almacenado...")
    return True

def recognite():
    """
    Usamos el modelo para reconocer rostros
    """
    imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)

    face_recognizer = cv2.face.FisherFaceRecognizer_create()

    # Leyendo el modelo
    face_recognizer.read('./modeloFisherFace.xml')

    # Capturamos video en vivo
    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    while True:
        ret,frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
           
            # FisherFace
            if result[1] < 500:
                nombre = imagePaths[result[0]]
                cv2.putText(frame,nombre,(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            else:
                nombre = "Desconocido"
                cv2.putText(frame,nombre,(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
           
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Experimental
# Función para reconocer rostros
def recognize_with_interface():
    """
    Usamos el modelo para reconocer rostros
    """
    imagePaths = os.listdir(dataPath)
    print('imagePaths=', imagePaths)

    face_recognizer = cv2.face_FisherFaceRecognizer.create()

    # Leyendo el modelo
    face_recognizer.read('./modeloFisherFace.xml')

    # Capturamos video en vivo
    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            # FisherFace
            if result[1] < 500:
                nombre = imagePaths[result[0]]
                cv2.putText(frame, nombre, (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                nombre = "Desconocido"
                cv2.putText(frame, nombre, (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return frame
    cap.release()

if __name__ == "__main__":
    # capture("Cris")
    # fit()
    recognite()
