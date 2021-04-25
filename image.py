import os, shutil
import pytesseract as pt
from PIL import Image
from pathlib import Path
import final
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'

async def process_files(Folder, msg):
    for root, _, folder in os.walk(Folder):
        for image in folder:
            fullpath = os.path.join(root, image)
            await process_file(fullpath, msg)

async def process_file(PathToFile, msg):
    result = ''
    
    print(PathToFile)
    image = Image.open(PathToFile)
    result = pt.image_to_string(image)
    result = result.lower()
        
    print(f'[IMAGE PROCESS] image scanning complete, results for {msg.id}: {result}')
    await final.scan_for_blacklisted_words(msg, result)
    
    if os.path.dirname(PathToFile).__contains__('spliced') and len(os.listdir(os.path.dirname(PathToFile))) == 0:
        shutil.rmtree(Path(PathToFile).parents[0])
    os.remove(PathToFile)