# %%
import re 
import requests
from bs4 import BeautifulSoup as bs
import os 
import pathlib

pathos = pathlib.Path(__file__).parent
os.chdir(pathos)

# %%


def ifnotmake(out_path):

    init = out_path.split("/")
    init = init[:-1]
    init = "/".join(init)

    if not os.path.exists(init):
        os.mkdir(init)

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    exists = os.path.exists(out_path)


# %%


def gettem(outpath, stemmo, pathos):
    ifnotmake(outpath)

    r = requests.get(pathos)

    soup = bs(r.text, 'html.parser')
 
    mp3_url = None
    for s in soup.select("script:not([src])"):
        text = s.string or s.get_text() or ""
        m = re.search(r'https?://[^\s"\']+\.mp3', text, flags=re.IGNORECASE)
        if m:
            mp3_url = m.group(0)
            break

    response = requests.get(mp3_url, stream=True)

    with open(f"{outpath}/{stemmo}.mp3", 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)



gettem('clips/2510/barnaby',
'michaelmccormack',
'https://www.abc.net.au/listen/programs/radionational-breakfast/mccormack-wants-joyce-to-live-out-days-as-a-nat/105909848'
)


# gettem('clips/2510/barnaby',
# 'murraywatt',
# 'https://www.abc.net.au/listen/programs/radionational-breakfast/government-edges-closer-to-new-environment-reforms/105909846'
# )



