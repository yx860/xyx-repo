import requests
import json
from pathlib import Path 
import pandas as pd
import time 

def main():
    #URL for api and the folder path to access mp3 files. Folder is asssumed to be stored in asr directory.
    url = "http://localhost:8001/asr"
    dir_path = Path(__file__).parent.parent/"cv-valid-dev"
    
    #CSV file is stored in the same folder as cv-decode.py
    csv_file = "cv-valid-dev.csv"
    #Path for the new CSV file.
    new_csv_file_path = Path(__file__).parent.parent/"deployment-design/elastic-backend/cv-valid-devtest.csv"
    
    tries = 5
    
    new_column_name = 'generated_text'
    csv_file = pd.read_csv('cv-valid-dev.csv')
    csv_file[new_column_name] = pd.NA
    
    # Open the file and send it in the POST request
    for i, mp3_file in enumerate(dir_path.glob('*.mp3')):
        for n in range(tries): 
            try:
                with open(mp3_file, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(url, files=files).json()
    
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
    
    #Store modified CSV file in new elastic-backend folder for indexing
    csv_file.to_csv(new_csv_file_path, index=False)

if __name__ == "__main__":
    main()
