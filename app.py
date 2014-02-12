from bottle import Bottle, route, run, request, redirect
import re

HASH_RE = re.compile(".+xt=urn:btih:([^&]+).*")
TOR_CACHE = "http://torrage.com/torrent/{}.torrent"

app = application = Bottle()

htmlblob = """<html>
                    <b><script type='text/javascript'>
                        function loadMagLink(frm){
                            window.location.assign('http://%s/?l=' + frm.maglink.value)
                        }
                    </script>
                    <form>
                        <p>%s<br/><br/>Needs to be of format http://%s/?l=[magnet link]</p>
                        Or, Enter the magnet link: <input type='text' name=maglink>
                        <input type='button' value='Convert' onclick='loadMagLink(this.form)'>
                    </form></b>
                </html>
           """

@app.route('/')
def index():
    link = request.query.get("l")
    if not link:
        return htmlblob % (request.urlparts.netloc, "No link provided", request.urlparts.netloc)

    temp = HASH_RE.match(link)
    if not temp:
        return htmlblob % (request.urlparts.netloc, "Invalid link provided", request.urlparts.netloc)

    do_link(temp.group(1))

def do_link(info_hash):
    # Can the filename be specified if something other than a redirect is used?

    redirect(TOR_CACHE.format(info_hash.upper()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
