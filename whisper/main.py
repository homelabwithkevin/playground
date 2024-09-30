import whisper
import re
from datetime import datetime

def get_date():
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print(now)
    return now

# Available models:
# tiny, base, small, medium, large

mp3_files = [
    'full_path.mp3'
]

enable_transcribe = True
model_version = 'medium'

for mp3_file in mp3_files:
    journal_file = mp3_file.split('\\')[-1].split('.')[0] + '.md'

    if enable_transcribe:
        get_date()
        model = whisper.load_model(model_version)
        result = model.transcribe(mp3_file)

        text_result = result['text']

        text_result_split = re.split('break. |Break. |Break |Break.|, break.| break | brake. | brake', text_result)

        with open(journal_file, 'a') as f:
            f.write('Whisper Transcription\n\n')

        for text in text_result_split:
            with open(journal_file, 'a') as f:
                f.write(text.strip() + '\n\n')

        get_date()
