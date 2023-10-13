import speech_recognition as sr

r = sr.Recognizer()

def microphone():
    with sr.Microphone() as source:
        print("Di algo...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='es-EC')
            print("Esto entendi: {}".format(text))

        except KeyboardInterrupt as e:
            print(text)

    return text

if __name__ == "__main__":
    microphone()