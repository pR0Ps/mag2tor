from bottle import Bottle, route, run, request, redirect
import re

HASH_RE = re.compile(".+xt=urn:btih:([^&]+).*")
TOR_CACHE = "http://torrage.com/torrent/{}.torrent"

app = application = Bottle()

@app.route('/')
def index():
    link = request.query.get("l")
    if not link:
        return "<html><b>No link provided<br/><br/>Try http://{}/?l=[magnet link]</b></html>".format(request.urlparts.netloc)

    temp = HASH_RE.match(link)
    if not temp:
        return "<html><b>Invalid link provided</b></html>"

    do_link(temp.group(1))

def do_link(info_hash):
    # Can the filename be specified if something other than a redirect is used?

    redirect(TOR_CACHE.format(info_hash.upper()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
