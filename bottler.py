
from bottle import Bottle, request, response
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, urlsplit, unquote
import html
import re


app = Bottle()

#### HELPERS

def is_abc_url(url: str) -> bool:
    try:
        return url.startswith("https://www.abc.net.au/")
    except Exception:
        return False


def find_mp3_url(page_url: str, timeout: int = 10) -> str | None:

    r = requests.get(
        page_url, timeout=timeout,
        headers={"User-Agent": "BottleFetcher/1.0 (+https://example.invalid)"}
    )
    r.raise_for_status()

    soup = bs(r.text, "html.parser")

    for tag in soup.select("audio[src], source[src]"):
        src = tag.get("src")
        if src and re.match(r"^https?://.+\.mp3(?:[?#].*)?$", src, flags=re.I):
            return src

    for s in soup.select("script:not([src])"):
        text = s.string or s.get_text() or ""
        m = re.search(r"https?://[^\s\"']+\.mp3", text, flags=re.I)
        if m:
            return m.group(0)

    return None

def stream_mp3(mp3_url: str, timeout: int = 15):
    upstream = requests.get(
        mp3_url, stream=True, timeout=timeout,
        headers={"User-Agent": "BottleFetcher/1.0 (+https://example.invalid)"}
    )
    upstream.raise_for_status()

    cl = upstream.headers.get("Content-Length")
    if cl and cl.isdigit():
        response.set_header("Content-Length", cl)

    response.content_type = upstream.headers.get("Content-Type", "audio/mpeg")

    response.set_header("Content-Disposition", f'attachment; filename="audio.mp3"')

    def generate():
        for chunk in upstream.iter_content(chunk_size=8192):
            if chunk:
                yield chunk
    return generate()

#### ROUTES

@app.get("/")
def index():
    return """
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#f7f7f7;margin:0;padding:0;">
      <div style="background:#fff;padding:24px 28px;border-radius:12px;box-shadow:0 6px 24px rgba(0,0,0,0.08);font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;max-width:640px;width:100%;">
        <h2 style="margin-top:0;margin-bottom:16px;text-align:center;">Let's fetch some audio!</h2>
        <form action="/fetch" method="post" style="display:flex;flex-direction:column;gap:12px;">
          <input type="text" id="url" name="url" placeholder="https://www.abc.net.au/..." style="width:100%;max-width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:8px;" required>
          <input type="submit" value="Submit" style="padding:10px 14px;border:0;border-radius:8px;background:#111;color:#fff;cursor:pointer;">
        </form>
        <p style="margin-top:12px;color:#666;font-size:0.9em;text-align:center;">
          Only URLs starting with <code>https://www.abc.net.au/</code> are allowed.
        </p>
      </div>
    </div>
    """

@app.post("/fetch")
def fetcher():
    url = (request.forms.get("url") or "").strip()

    if not url:
        response.status = 400
        return "Missing URL."
    if not is_abc_url(url):
        response.status = 400
        return "Please provide a URL starting with https://www.abc.net.au/."

    # If the input is already a direct .mp3, stream it
    if re.search(r"\.mp3(?:[?#].*)?$", url, flags=re.I):
        try:
            return stream_mp3(url)
        except requests.exceptions.RequestException as e:
            response.status = 502
            return f"Failed to fetch MP3: {html.escape(str(e))}"

    # Otherwise, discover the mp3 from the page and stream it
    try:
        mp3_url = find_mp3_url(url)
    except requests.exceptions.RequestException as e:
        response.status = 502
        return f"Failed to fetch page: {html.escape(str(e))}"

    if not mp3_url:
        response.status = 404
        return "Could not find an .mp3 URL on that page."

    try:
        return stream_mp3(mp3_url)
    except requests.exceptions.RequestException as e:
        response.status = 502
        return f"Failed to fetch MP3: {html.escape(str(e))}"



if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True, reloader=True)
