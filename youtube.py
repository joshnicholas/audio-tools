import os 


def grabber(out_path, stemmo, pathos):
    os.system(f"yt-dlp --extract-audio --audio-format mp3 --output '{out_path}/{stemmo}.mp3' '{pathos}'")




# grabber('clips/2510/barnaby',
# "joyce_johnny_depp_dogs",
# 'https://www.youtube.com/watch?v=SxOr7Brscpw'
# )


grabber('clips/2510/barnaby',
"seven_joyce_lying_on_street",
'https://www.youtube.com/watch?v=eM5RFxTgSmk'
)


