from fastapi import FastAPI, File, UploadFile
import uvicorn
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC
import torch
import torchaudio
from mutagen.mp3 import MP3
from io import BytesIO

app = FastAPI()

processor = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

@app.get("/ping")
async def pong():
    return "pong"

@app.post("/asr")
async def create_upload_file(file: UploadFile = File(...)):

    # if file.content_type != "text/plain":
    #     return JSONResponse(status_code=400, content={"message": "Invalid file type. Only text files are accepted."})
    audio_data = BytesIO(await file.read())
    waveform, sample_rate = torchaudio.load(audio_data, format="mp3")
    
    #ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
    mp3_audio = MP3(audio_data)
    duration = mp3_audio.info.length


    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        
    # Ensure the waveform is mono (single channel)
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # tokenize
    input_values = processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=16000)  # Batch size 1
    
    # retrieve logits
    logits = model(**input_values).logits
    
    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    print(transcription)
    return {
        "transcription": transcription, 
        "duration": duration
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
