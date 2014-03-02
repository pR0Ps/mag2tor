from bottle import Bottle, route, run, request, redirect
import re

HASH_RE = re.compile(".+xt=urn:btih:([^&]+).*")
TOR_CACHE = "http://torrage.com/torrent/{}.torrent"

app = application = Bottle()

htmlblob = """<html>
                    <b><form>
                        <p>{0}<br/><br/>Needs to be of format http://{1}/?l=[magnet link]</p>
                        Or, Enter the magnet link: <input type='text' name=l>
                        <input type='Submit' value='Convert'>
                    </form></b>
                </html>
           """

@app.route('/')
def index():
    link = request.query.get("l")
    if not link:
        return htmlblob.format("No link provided", request.urlparts.netloc)

    temp = HASH_RE.match(link)
    if not temp:
        return htmlblob.format("Invalid link provided", request.urlparts.netloc)

    redirect(TOR_CACHE.format(temp.group(1).upper()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
