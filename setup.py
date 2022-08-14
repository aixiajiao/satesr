import os
import zipfile
os.system("python -m pip install --upgrade pip")
os.system('pip3 install torch torchvision torchaudio')
os.system('pip3 install requests Pillow urllib3 tqdm basicsr')
from sate_api.dataloaders import download



model_url = 'https://onedrive.live.com/download?cid=1FBE8A2F75A20AE8&resid=1FBE8A2F75A20AE8%21196323&authkey=AEcdm82rcVJ8lFo'
fname='srmodels.zip'
dirPath = 'models'
# Delete all contents of a directory using shutil.rmtree() and  handle exceptions
#try:shutil.rmtree(dirPath)
#except: print('Downloading Models')

if not os.path.exists(dirPath):
    print('Downloading Models')
    download(model_url,fname)
    try:
        with zipfile.ZipFile(fname) as z:
            z.extractall()
            print("Models Extracted")
        os.remove(fname)
    except:
        print("Models Extraction Failed")