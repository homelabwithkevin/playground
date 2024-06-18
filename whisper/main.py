import whisper
import re

# Available models:
# tiny, base, small, medium, large

# Initial
# model = whisper.load_model("tiny")

# Actual
model = whisper.load_model("small")

result = model.transcribe("2024-06-18.mp3")

text_result = result['text']

print(text_result)

text_result_split = re.split('break. |Break. |Break |Break.', text_result)

for text in text_result_split:
    with open('journal.txt', 'a') as f:
        f.write(text.strip() + '\n\n')
