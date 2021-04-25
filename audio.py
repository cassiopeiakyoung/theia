import speech_recognition as SpeechRec
from pydub.silence import split_on_silence
from pydub import AudioSegment
import os
import final

recognize = SpeechRec.Recognizer()

def process_file(PathToFile, msg):
    result = ''
    
    sound = AudioSegment.from_mp3(PathToFile)
    spliced = split_on_silence(sound, min_silence_len = 500, silence_thresh = sound.dBFS-14, keep_silence = 500)
    folder = 'temp/spliced-'+(str(msg.id))
    os.mkdir(folder)
    
    for i, currentClip in enumerate(spliced, start = 1):
        spliced_segment = os.path.join(folder, f'spliced{i}.wav')
        currentClip.export(spliced_segment, format = 'wav')
        
        with SpeechRec.AudioFile(spliced_segment) as source:
            clipFinished = recognize.record(source)
            
            try:
                currentConv  = SpeechRec.recognize_google(clipFinished)
            except SpeechRec.UnknownValueError as error:
                print(f'[AUDIO PROCESS] error:{str(error)}')
            else:
                result += currentConv.lower()
    
    print(result)