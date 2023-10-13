import speech_recognition as sr

r = sr.Recognizer()

def microphone():
    with sr.Microphone() as source:
        print("Say Something...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='es-EC')
            print("What did you say: {}".format(text))

        except KeyboardInterrupt as e:
            print(text)

    return text

if __name__ == "__main__":
    microphone()