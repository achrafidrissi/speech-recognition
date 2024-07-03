from pydub import AudioSegment

audio = AudioSegment.from_file("output.wav")

#increase the volume by 6 db
audio = audio + 6
audio = audio * 2
audio = audio.fade_in(2000)

audio.export("mahup.mp3", format="mp3")

audio2 = AudioSegment.from_wav("output.wav")
print("done")