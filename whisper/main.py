import whisper
import re

# Available models:
# tiny, base, small, medium, large

mp3_file = '2024-06-25.mp3'
journal_file = mp3_file.split('\\')[-1].split('.')[0] + '.md'

enable_transcribe = True

if enable_transcribe:
    model = whisper.load_model("medium")
    result = model.transcribe(mp3_file)

    text_result = result['text']

    text_result_split = re.split('break. |Break. |Break |Break.|, break.| break ', text_result)

    with open(journal_file, 'a') as f:
        f.write('Whisper Transcription\n\n')

    for text in text_result_split:
        with open(journal_file, 'a') as f:
            f.write(text.strip() + '\n\n')