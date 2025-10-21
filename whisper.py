import mlx_whisper


# pathos = '/Users/josh_nicholas/Audio/251020_barnaby/cut_clips/murraywatt.wav'

# pathos = '/Users/josh_nicholas/Audio/251020_barnaby/cut_clips/mccormackmain.wav'

pathos = '/Users/josh_nicholas/Audio/251020_barnaby/cut_clips/joyce_rn_headline.wav'

# pathos = '/Users/josh_nicholas/Downloads/Pauline Hanson grab.mp3'

pathos = '/Users/josh_nicholas/Downloads/Joyce RN breakfast.mp3'

text = mlx_whisper.transcribe(pathos)["text"]

print(text)


