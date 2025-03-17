import pyttsx3
from chatgpt_api import ChatGPTAPI
from rag_model import get_advice  # Ensure this is correctly imported
from transcription import Transcription
from response_generator import ResponseGenerator
from speech_recog import start_listening
from emotion_recognition import detect_emotion

class VoiceAssistant:
    def __init__(self):
        self.user_name = ""
        self.emotion_recognition = detect_emotion
        self.transcription = Transcription()
        self.chatgpt = ChatGPTAPI()
        self.response_generator = ResponseGenerator()
        self.engine = pyttsx3.init()  # Initialize text-to-speech engine
        
        # Get available voices and set a female voice if available
        voices = self.engine.getProperty('voices')
        if voices:
            # Option 1: Directly use the second voice if it exists (often a female voice)
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[2].id)
            # Option 2: Alternatively, search for a voice with 'female' in its name
            else:
                for voice in voices:
                    if 'female' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break

    def speak(self, text):
        """Speak the given text using pyttsx3."""
        self.engine.say(text)
        self.engine.runAndWait()

    def start_conversation(self):
        """Starts the conversation by immediately asking for advice."""
        welcome_message = "Hello! What advice do you need today?"
        print(welcome_message)
        self.speak(welcome_message)
        self.ask_for_advice()

    def listen_to_user(self):
        """Capture user input via voice."""
        return start_listening()

    def ask_for_advice(self):
        """Directly ask for advice without selecting a category."""
        prompt = "Tell me what’s on your mind, and I’ll give you some advice."
        print(prompt)
        self.speak(prompt)
        
        user_input = self.listen_to_user()
        emotion = self.emotion_recognition(user_input)
        print(f"my current emotion is {emotion}")
        user_input_with_emotion = f"{user_input}, my current emotion is {emotion}"        # Use RAG to get advice
        response_data = get_advice(user_input_with_emotion)

        # Convert string response to a dictionary if needed
        if isinstance(response_data, str):
            response_data = {"answer": response_data}

        # advice = response_data.get("answer", "I'm not sure how to respond.")
        # # emotion = self.analyze_emotion(user_input)
        # response = self.generate_response(advice, emotion)

        # Print and speak the generated response
        print(response_data['answer'])
        # Transcribe the conversation for logging or future reference
        self.transcribe_conversation(user_input,response_data['answer'])
        self.speak(response_data['answer'])



    def transcribe_conversation(self, user_input, bot_response):
        """Transcribe the conversation to JSON or log."""
        self.transcription.transcribe(user_input, bot_response)
        self.transcription.save_transcript()

    # def analyze_emotion(self, user_input):
    #     """Perform emotion recognition based on user input."""
    #     return self.emotion_recognition.recognize(user_input)

    def generate_response(self, advice, emotion):
        """Generate a response based on ChatGPT advice and detected emotion."""
        return self.response_generator.generate_response(advice, emotion)