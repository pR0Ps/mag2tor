from bottle import Bottle, route, run, request, redirect
import re

HASH_RE = re.compile(".+xt=urn:btih:([^&]+).*")
TOR_CACHE = "http://torrage.com/torrent/{}.torrent"

app = application = Bottle()

htmlblob = """
<html>
  <head>
    <title>Mag2Tor</title>
  </head>
  <body>
    <p>This service will take a magnet link and allow you to save the corresponding torrent file.</p>
    <form>
      <p>Enter the magnet link: <input type='text' name=l>
      <input type='Submit' value='Convert'></p>
    </form>
    <p>{0}</p>
</html>"""

@app.route('/')
def index():
    link = request.query.get("l")
    if not link:
        return htmlblob.format("")

    temp = HASH_RE.match(link)
    if not temp:
        return htmlblob.format("ERROR: Invalid link provided")

    redirect(TOR_CACHE.format(temp.group(1).upper()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
