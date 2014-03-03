from bottle import Bottle, route, run, request, redirect
import re

HASH_RE = re.compile(".+xt=urn:btih:([^&]+).*")
TOR_CACHE = "http://torrage.com/torrent/{}.torrent"

app = application = Bottle()

htmlblob = """
<DOCTYPE HTML>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <meta name="description" content="Magnet link to torrent converter">
    <meta name="keywords" content="magnet, torrent, convert, converter">
    <title>Mag2Tor</title>
    <style type="text/css">
      body {{
        color: #000000;
        background-color: #FFFFFF;
        text-decoration: none;
        font-family: 'arial', 'sans-serif';
      }}
      main {{
        text-align: center;
        margin-top: 100px;
      }}
      img#gh-banner {{
        position: absolute;
        top: 0;
        right: 0;
        border: 0;
      }}
      p#error {{
        color: #FF0000;
        display: none; /* for now */
      }}
      footer {{
          position: absolute;
          bottom: 50px;
          right: 50px;
      }}
      input {{
        padding:5px 15px;
        -webkit-border-radius: 5px;
        border-radius: 5px;
      }}
      input[type=text] {{
        width: 570px;
        border:2px solid
        border-color: #ccc;
      }}
      input[type=text]:focus {{
        border-color:#333;
      }}
      input[type=submit] {{
        cursor:pointer;
        background:#ccc;
        border: 2px none;
        margin: 10px 5px 10px 5px;
        height: 30px;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>Mag2Tor</h1>
      <a href="https://github.com/pR0Ps/mag2tor"><img id="gh-banner" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>
      <p>Enter a magnet link below to be redirected to the corresponding torrent file.</p>
      <form>
        <input type='text' placeholder='Magnet link' name='l'><br>
        <input type='Submit' value='Convert'>
      </form>
    </main>
    <p id='error' >{0}</p>
    <footer>Made by <a href="http://cmetcalfe.ca">Carey Metcalfe</a></footer>
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
