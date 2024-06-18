import whisper
import re

# Available models:
# tiny, base, small, medium, large

# Initial
# model = whisper.load_model("tiny")

# Actual
model = whisper.load_model("medium")

result = model.transcribe("2024-06-18.mp3")

text_result = result['text']

text_result_split = re.split('break. |Break. |Break |Break.', text_result)

with open('journal.txt', 'a') as f:
    f.write('Whisper Transcription\n\n')

for text in text_result_split:
    with open('journal.txt', 'a') as f:
        f.write(text.strip() + '\n\n')
