import requests
import time
import pprint
import json
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES

transcription_endpoint = "https://api.assemblyai.com/v2/transcript"
headers_assemblyai = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

listennotes_episode_endpoint = 'https://listen-api.listennotes.com/api/v2/episodes'
listennotes_headers = {'X-ListenAPI-Key': API_KEY_LISTENNOTES}

#listenotes.ai

def get_episode_audio_url(episode_id):
    url = listennotes_episode_endpoint + '/' + episode_id
    response = requests.request('GET', url, headers = listennotes_headers)

    data = response.json()
    pprint.pprint(data)

    audio_url = data['audio']
    episode_title = data['title']
    thumbnail = data['thumbnail']
    podcast_title = data['podcast']['title']



    return audio_url, thumbnail, podcast_title, episode_title

#transcribe
def transcribe(audio_url, auto_chapters):
    transcript_request = { "audio_url": audio_url, 'auto_chapters': auto_chapters }
    transcript_response = requests.post(transcription_endpoint, json=transcript_request, headers=headers_assemblyai)
    job_id = transcript_response.json()['id']
    return job_id



#polling
def poll(transcript_id):
    polling_endpoint = transcription_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers_assemblyai)
    return polling_response.json()

#asking assembly.ai if transcription is done
def get_transcription_result_url(audio_url, auto_chapters):
    transcript_id = transcribe(audio_url, auto_chapters)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
    
        print('Waiting 30 seconds...')
        time.sleep(30)




#save transcript

def save_transcript(audio_url, filename):

    data,error = get_transcription_result_url(audio_url)

    if data:
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data['text'])
        print('Transcription Saved!!')
    elif error:
        print('there was an error!')
    print(data)
