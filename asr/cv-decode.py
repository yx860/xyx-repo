import requests
import json
from pathlib import Path 
import pandas as pd
import time 

# Define the URL and the file path
url = "http://localhost:8001/asr"
dir_path = Path(__file__).parent.parent/"cv-valid-dev"
csv_file = "cv-valid-dev.csv"

tries = 5

new_column_name = 'generated_text'
csv_file = pd.read_csv('cv-valid-dev.csv')
csv_file[new_column_name] = pd.NA

# Open the file and send it in the POST request
for i, mp3_file in enumerate(dir_path.glob('*.mp3')):
    # if i == 5:
    #     break
    for n in range(tries): 
        try:
            with open(mp3_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files).json()

            # capped to the first 5 mp3 files in the folder for testing purpose   
            

            #obtain the transcription and write into new CSV file  
            transcription = response['transcription']
            print(transcription)
            print(response['duration'])
            csv_file.at[i, 'duration'] = response['duration']
            csv_file.at[i, new_column_name] = transcription
            break
        except Exception as e:
            print(e)
            time.sleep(2*n)

#overwrite CSV file with the new data 
csv_file.to_csv('cv-valid-dev.csv', index=False)


