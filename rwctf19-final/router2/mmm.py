from flask import Flask
from flask import render_template,request,redirect
 
app = Flask(__name__)
 
@app.route('/')
def test():
    return '''
<script>
    alert("pwned by slipper");
    setTimeout(function() {
        location.href = 'https://douyu.com/exploit'
    }, 3000)
</script>
<h3>pwned by slipper??</h3>'''

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
