import sys
from api_communication import *
import streamlit as st
import pyaudio
import wave

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
def record_audio(filename, seconds=5):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    st.write("Recording...")
    frames = []

    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    st.write(f"Saved recording to {filename}")

def main():
    st.title("Audio Transcription with AssemblyAI")

    choice = st.radio("Choose an option", ["Record Audio", "Upload Audio File"])

    if choice == "Record Audio":
        if st.button("Record"):
            record_audio("output.wav", seconds=5)
            audio_url = upload("output.wav")
            data, error = get_transcription_result_url(audio_url)
            if data:
                st.write("Transcription:")
                st.write(data['text'])
            elif error:
                st.write("Error:", error)

    elif choice == "Upload Audio File":
        uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
        if uploaded_file is not None:
            with open("uploaded_audio.wav", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.write("Saved uploaded file to uploaded_audio.wav")
            audio_url = upload("uploaded_audio.wav")
            data, error = get_transcription_result_url(audio_url)
            if data:
                st.write("Transcription:")
                st.write(data['text'])
            elif error:
                st.write("Error:", error)

if __name__ == "__main__":
    main()

