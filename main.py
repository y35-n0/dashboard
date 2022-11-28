from flask import Flask, render_template, request
import pandas as pd
import json


data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
data_df = pd.DataFrame(data)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)