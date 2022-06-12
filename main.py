import streamlit as st
import glob
import json
from api_communication import save_transcript

st.title("Podcast Summaries")
st.markdown("Mini project by Dylan Huey")

json_files = glob.glob('*.json')

episode_id = st.sidebar.text_input("Episode ID")
directions = st.sidebar.header("How to obtain episode id:")
step_one = st.sidebar.subheader("- Locate episode on [listennotes.com](https://www.listennotes.com/)")
step_two = st.sidebar.subheader("- In the bottom right click 'Use API to fetch this episode'")
step_three = st.sidebar.subheader("- Copy and paste the episode id into the text input")
step_four = st.sidebar.subheader("- Click the 'Generate summary' button")
button = st.sidebar.button("Generate Episode summary", on_click=save_transcript, args=(episode_id,))
time = st.sidebar.write("Depending on episode length it may take multiple minutes to generate result")

def get_clean_time(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
        
    return start_t


if button:
    filename = episode_id + '_chapters.json'
    print(filename)
    with open(filename, 'r') as f:
        data = json.load(f)

    chapters = data['chapters']
    episode_title = data['episode_title']
    thumbnail = data['thumbnail']
    podcast_title = data['podcast_title']
    audio = data['audio_url']

    st.header(f"{podcast_title} - {episode_title}")
    st.image(thumbnail, width=200)
    st.subheader(f'{episode_title}')
    st.markdown(f"Episode length: {get_clean_time(chapters[-1]['end'])}")

    for chp in chapters:
        with st.expander(chp['gist'] + ' - ' + get_clean_time(chp['start'])):
            chp['summary']