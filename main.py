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
len(data_df['customerID'])

len(data_df[data_df['tenure'] <= 1])

len(data_df[data_df['Churn'] == 'Yes'])

data_df['tenure'].values.mean()
data_df['tenure'].values.mean().round(1)
data_df['InternetService'].value_counts()
data_df['InternetService'] = data_df['InternetService'].apply(lambda x: 'Yes' if x == 'DSL' or x == 'Fiber optic' else 'No')
data_df['InternetService'].value_counts()
data_df['OnlineSecurity'].value_counts()
data_df['OnlineSecurity'] = data_df['OnlineSecurity'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')
data_df['OnlineBackup'].value_counts()
data_df['OnlineBackup'] = data_df['OnlineBackup'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')
data_df['OnlineSecurity']

data_df['Internet'] = int(0)
data_df['Internet'].value_counts()
data_df = data_df
for i in range(len(data_df)):
    if data_df['InternetService'][i] == 'Yes' or data_df['OnlineSecurity'][i] == 'Yes' or data_df['OnlineBackup'][i] == 'Yes':
        data_df['Internet'][i] = 'Yes'
    else:
        data_df['Internet'][i] = 'No'
data_df['Internet'].value_counts()
data_df['StreamingTV'].value_counts()
data_df['StreamingTV'] = data_df['StreamingTV'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')
data_df['StreamingMovies'].value_counts()
data_df['StreamingMovies'] = data_df['StreamingMovies'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')
data_df['Streaming'] = 0
for i in range(len(data_df)):
    if data_df['StreamingTV'][i] == 'Yes' or data_df['StreamingMovies'][i] == 'Yes':
        data_df['Streaming'][i] = 'Yes'
    else:
        data_df['Streaming'][i] = 'No'
data_df['Streaming'].value_counts()

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/customerinfo') 
def customerinfo():
    result = {"totalcus" : len(data_df['customerID']),
                "newcus": len(data_df[data_df['tenure'] <= 1]),
                "churncus": len(data_df[data_df['Churn'] == 'Yes']),
                "avgdur" : data_df['tenure'].values.mean().round(1)}
    result = json.dumps(result)
    return result

data_df.Internet.unique()

@app.route('/onlinepie') #사용자 정의 필터
def onlinepie():
    df = data_df.Internet
    fig = px.pie(df, values='Internet', names=df.unique().tolist())
    fig.show()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('onlinepie.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)