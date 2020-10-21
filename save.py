import os
import requests

from fastapi import HTTPException

path = './storage'

def save_img(patient, url, current):
    directories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    if patient not in directories:
        os.mkdir(os.path.join(path, str(patient)))
    try:    # Try-except for download error handling (failing to download or file non-found).
        r = requests.get(url, allow_redirects=True)
    except:
        raise HTTPException(status_code=404, detail="Download failed or file not found.")
    name = './storage/' + str(patient) + '/' + str(patient) + '_' + current + '.jpg'
    open(name, 'wb').write(r.content)
    return name