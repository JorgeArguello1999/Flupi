import speech_recognition as sr

r = sr.Recognizer()

def microphone():
    with sr.Microphone() as source:
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='es-EC')

        except Exception as e:
            text = ""
            print(f"Error: {e}")

    return text

if __name__ == "__main__":
    microphone()