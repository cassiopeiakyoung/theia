import os, cv2, shutil, moviepy
import final, image, audio, dispatcher


async def process_file(PathToFile, msg):
    capture = cv2.VideoCapture(PathToFile)
    folder = 'temp/spliced-'+(str(msg.id))
    os.mkdir(folder)
    
    i = 0
    while(capture.isOpened()):
        r, frame = capture.read()
        
        if not r:
            break
        
        cv2.imwrite(f'{folder}/{str(i)}.jpg', frame)
        i += 1
    
    if dispatcher.header_type(msg.content) == 'VIDEO':
        audioToBeSent = moviepy.editor.VideoFileClip(PathToFile).audio
        audioToBeSent.write_audiofile(f'temp/AUDIO-SPLIT{msg.id}.mp3')
        await audio.process_file(f'temp/AUDIO-SPLIT{msg.id}.mp3', msg)
    
    await image.process_files(folder, msg)