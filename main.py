from flask import Flask, render_template, request
from mysql.connector import  pooling
from base64 import b64encode
from datetime import datetime
import pandas as pd
import plotly
import plotly.express as px
import json


data = pd.read_csv('C:/Users/NTX550/Desktop/ASAC/web/WA_Fn-UseC_-Telco-Customer-Churn.csv')
data_df = pd.DataFrame(data)
print(data_df)
len(data_df)

len(data_df[data_df['tenure'] <= 1])

len(data_df[data_df['Churn'] == 'Yes'])

data_df['tenure'].values.mean()

data_df['Internet'] = data_df['InternetService'].apply(lambda x: 'Yes' if x == '')


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/customerinfo') 
def customerinfo():
    result = {"totalcus" : 7043,
                "newcus": 624,
                "churncus": 1869,
                "avgdur" : 32.4}
    result = json.dumps(result)
    return result

@app.route('/newcustomer') 
def newcustomer():
    return render_template('newcustomer.html')

@app.route('/churncustomer') 
def churncustomer():
    return render_template('churncustomer.html')

@app.route('/avgduration') 
def avgduration():
    return render_template('avgduration.html')

@app.route('/birthChart') #사용자 정의 필터
def birthChart():
    
    graphJSON = json.dumps( fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('nodash2.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)