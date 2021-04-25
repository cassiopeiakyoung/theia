import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os, shutil
import final

r = sr.Recognizer()

async def process_file(PathToFile, msg):
    result = ''
    
    sound = AudioSegment.from_mp3(PathToFile)  
    settings = split_on_silence(sound, min_silence_len = 500, silence_thresh = sound.dBFS-14, keep_silence = 500)
    folder = 'temp/spliced-'+(str(msg.id))

    os.mkdir(folder)

    for i, chunk in enumerate(settings, start=1):
        filechunk = os.path.join(folder, f'chunk{i}.wav')
        chunk.export(filechunk, format='wav')

        with sr.AudioFile(filechunk) as source:
            current = r.record(source)

            try:
                text = r.recognize_google(current)
            except sr.UnknownValueError as Error:
                print(f'[AUDIO PROCESS] error:{str(Error)}')
            else:
                text = f'{text.lower()} '
                result += text
    print(f'[AUDIO PROCESS] audio scanning complete, results for {msg.id}: {result}')
    await final.scan_for_blacklisted_words(msg, result)
    
    shutil.rmtree(folder)
    os.remove(PathToFile)