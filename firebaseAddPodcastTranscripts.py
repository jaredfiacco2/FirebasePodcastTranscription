import requests
import os
from pydub import AudioSegment
import pandas as pd
import speech_recognition as sr
from pydub.silence import split_on_silence
import firebase_admin
from firebase_admin import credentials, firestore

# # Firebase Credentials
# cred = credentials.Certificate("darknetdiaries-firebase-adminsdk-cmlo5-0476cd885a.json")
# app = firebase_admin.initialize_app(cred)
# store = firestore.client()

def transcribeNewPodcasts(store):
    # Get 
    # docs = store.collection(u'item').where(u'`itunes:episode`', u'<=', '2').stream()
    docs = store.collection(u'item').stream()
    for doc in docs:
        df              = doc.to_dict()
        curEpId         = doc.id
        curEpNumber     = df['itunes:episode']
        curEpTitle      = df['title'].replace(':', '').replace(' ', '_')
        curEpMp3        = df['guid.#text']
        curEpMp3Path    = 'mp3\\'+ curEpTitle +'.mp3'
        curEpWavPath    = 'wav\\'+ curEpTitle +'.wav'
        print(curEpMp3)
        print(curEpWavPath)
        print(curEpId)
        countTranscriptIds = 0
        transcript_stream = store.collection(u'item').document(curEpId).collection(u'transcript').stream()
        for trans in transcript_stream:
            countTranscriptIds += 1
        if countTranscriptIds > 0:
            print('Already did this, next!')
            continue
        if curEpId == 'qJcNdu4qWDdJ5WSQgj2R' or curEpId == 'vICcrIy5abuF94Al73Yz':
            print('This one wont work for some reason :(')
            continue   

        # Download MP3
        # Document ID: DrQccrQQSpyk8CphettH
        doc = requests.get(curEpMp3)
        with open(curEpMp3Path, 'wb') as f:
            f.write(doc.content)
        
        # Convert mp3 file to wav file
        # Following how to from here: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
        input_file = curEpMp3Path
        output_file = curEpWavPath
        sound = AudioSegment.from_mp3(input_file)
        sound.export(output_file, format="wav")
        if os.path.exists(input_file):
            os.remove(input_file)

        # create a speech recognition object
        r = sr.Recognizer()
        path = output_file
        data = {
                    'StartTime' : [], 
                    'EndTime' : [], 
                    # 'Type' : [],
                    'FrameRate' : [],
                    'Channels' : [],
                    'SampleWidth' : [],
                    'MaxAmplitude' : [],
                    'Length' : []
                }
        startTime = 0
        df = pd.DataFrame(data)

        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)  
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 500,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        folder_name = "audio-chunks"
        startTime = 0
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            chunk_file = AudioSegment.from_file(file = chunk_filename, format='wav')
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                # try converting it to text
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    text = "Error"
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    whole_text += text
                newRow = {
                    'StartTime' : int(startTime), 
                    'EndTime' : int(startTime + len(chunk_file)), 
                    'FrameRate' : chunk_file.frame_rate,
                    'Channels' : int(chunk_file.channels),
                    'SampleWidth' : int(chunk_file.sample_width),
                    'MaxAmplitude' : int(chunk_file.max),
                    'Length' : int(len(chunk_file)),
                    'Text' : str(text)
                }
                df = df.append(newRow, ignore_index=True)
                startTime += len(chunk_file)
                print(newRow)
        # #Incase you want to save the transcripts in csv or json for debugging
        # df.to_json('transripts/json/' + curEpId +'.json', orient="index")
        # df.to_csv('transcripts/csv/' + curEpId +'.csv')
        df.to_pickle('pkl/transcripts/' + curEpId + ".pkl")

        if os.path.exists(output_file):
            os.remove(output_file)


        # Load df into firebase 
        item_transcript = df.to_dict(orient='records')
        doc_ref_transcript = store.collection(u'item').document(curEpId).collection(u'transcript')
        list(map(lambda x: doc_ref_transcript.add(x), item_transcript))
    return