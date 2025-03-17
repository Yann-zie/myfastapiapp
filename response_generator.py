class ResponseGenerator:
    def __init__(self):
        pass

    def generate_response(self, advice, emotion):
        # Generate a response that adjusts based on emotion
        if emotion['emotion'] == 'sad':
            return f"Hey, it's okay! Here's some advice: {advice}. Take care!"
        elif emotion['emotion'] == 'happy':
            return f"Awesome! Here's some advice: {advice}. Keep up the great work!"
        else:
            return f"Here's some advice: {advice}"
