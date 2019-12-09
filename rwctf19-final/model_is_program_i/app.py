#!/usr/bin/env python3

import subprocess
import tempfile

from flask import Flask, request

app = Flask("model-is-program-1")
app.config["MAX_CONTENT_LENGTH"] = 30*1024*1024

@app.route("/")
def index():
  return '''
  <!DOCTYPE html>
  <html>
  <head>
    <title>Patch Validator</title>
  </head>
  <body>
  <h1>Welcome!</h1>
  <p>We are running a copy of the patch validator for service ai-han-solo of DEF CON 27 CTF.</p>
  <p>This service is designed by hackers, for hackers, it must be safe.</p>

  <h2>Upload your patch</h2>
  <form action="/patch" method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit" value="Upload!">
  </form>
  </body>
  </html>
  '''

@app.route("/patch", methods=["POST"])
def patch():
  if "file" not in request.files:
    return "No file selected."
  uf = request.files["file"]
  if not uf.filename:
    return "No file selected."
  with tempfile.NamedTemporaryFile("wb") as tmpf:
    uf.save(tmpf)
    tmpf.flush()
    # check_filetype.sh
    check_result = subprocess.check_output(["/usr/bin/file", tmpf.name])
    if b"Hierarchical Data Format (version 5) data" not in check_result:
      return "PUBLIC: incorrect patch file type. what are you doing?"
    # validate.sh
    try:
      val_result = subprocess.check_output([
          "/usr/bin/python3", "/ai_han_solo.py", "verify-navigation-parameters",
          "-m", tmpf.name, "-d", "/tmp/coordinates", "-n", "1",
      ])
    except subprocess.CalledProcessError as exc:
      return f"({exc.returncode}) {exc.output.decode('utf-8')}"
    return val_result.decode("utf-8")
