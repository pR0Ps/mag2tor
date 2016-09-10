#!/usr/bin/env python

from bottle import Bottle, route, run, request, redirect
import re

HASH_RE = re.compile(".+xt=urn:btih:([^&]+).*")
TOR_CACHE = "https://itorrents.org/torrent/{}.torrent"

app = application = Bottle()

HTMLBLOB = """
<!DOCTYPE HTML>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <meta name="description" content="Magnet link to torrent converter">
    <meta name="keywords" content="magnet, torrent, convert, converter">
    <meta name="viewport" content="width=device-width">
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
      a#title{{
        color: #000000;
        text-decoration: none;
      }}
      img#gh-banner {{
        position: absolute;
        top: 0;
        right: 0;
        border: 0;
      }}
      footer {{
        padding: 25px;
        text-align: center;
      }}
      input {{
        padding:5px 15px;
        -webkit-border-radius: 5px;
        border-radius: 5px;
        border:2px solid;
      }}
      input[type=text] {{
        max-width: 570px;
        width: 80%;
        border-color: #555555;
      }}
      input[type=text].error {{
        border-color: #FF0000;
      }}
      input[type=submit] {{
        cursor:pointer;
        font-weight: bold;
        background:#C0C0C0;
        margin: 10px 5px 10px 5px;
      }}
    </style>
  </head>
  <body>
    <main>
      <a href="/" id='title'><h1>Mag2Tor</h1></a>
      <a href="https://github.com/pR0Ps/mag2tor"><img id="gh-banner" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>
      <p>Enter a magnet link below to be redirected to the corresponding torrent file.</p>
      <form>
        <input type='text' placeholder='{0}' name='l' {1}><br>
        <input type='Submit' value='Convert'>
      </form>
    </main>
    <footer>Made by <a href="http://cmetcalfe.ca">Carey Metcalfe</a></footer>
</html>"""

def display(error_text=None):
    if error_text:
        return HTMLBLOB.format("ERROR: {0}".format(error_text), "class='error'")
    else:
        return HTMLBLOB.format("Enter a magnet link", "")

@app.route('/')
def index():
    link = request.query.get("l")
    if not link:
        return display()

    temp = HASH_RE.match(link)
    if not temp:
        return display("Invalid link provided")

    redirect(TOR_CACHE.format(temp.group(1).upper()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
