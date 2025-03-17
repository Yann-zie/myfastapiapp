import json
import os

class Transcription:
    def __init__(self):
        self.transcript = []

    def transcribe(self, user_input, bot_response):
        # Add user input and bot response to the transcript
        self.transcript.append({"user": user_input, "bot": bot_response})

    def save_transcript(self):
        filename = 'conversation.json'
        # Load existing data if file exists and is not empty
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    existing_transcript = json.load(f)
            except json.JSONDecodeError:
                # In case the file is empty or corrupted
                existing_transcript = []
        else:
            existing_transcript = []

        # Combine existing transcript with new entries
        combined_transcript = self.transcript + existing_transcript 

        # Save the combined transcript back to the file
        with open(filename, 'w') as f:
            json.dump(combined_transcript, f, indent=4)

        # Clear the current session's transcript if desired
        self.transcript = []