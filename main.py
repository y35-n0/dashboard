from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/customerinfo') 
def customerinfo():
    result = {"totalcus" : 7043,
                "newcus": 624,
                "churncus": 1869,
                "avgdur" : 32.4
                }
    result = json.dumps(result)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)