import speech_recognition as sr
def start_listening():
    """
    Captures audio input, processes it into text, and detects the associated emotion.
    Returns the transcribed text and the detected emotion.
    """
    recognizer = sr.Recognizer()   
    # Ensure microphone input works properly
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Handles background noise
            print("Listening...")            
            try:
                # Listen with a timeout to avoid indefinite waiting
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                user_input = recognizer.recognize_google(audio)
                # print(f"You said: {user_input}")                
                # # Detect emotion from the recognized text
                # emotion = EmotionRecognition()
                # print(f"Detected emotion: {emotion}")                
                # return f"{user_input} (Emotion: {emotion})"     
                return user_input       
            except sr.UnknownValueError:
                print("Could not understand the audio. Please try again.")
                return "Error: Unable to recognize speech."            
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return f"Error: {e}"    
    except OSError as os_err:
        print(f"Microphone error: {os_err}")
        return f"Error: Microphone issue ({os_err})"
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return f"Error: {ex}"

