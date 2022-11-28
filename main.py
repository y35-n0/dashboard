from flask import Flask, render_template
import pandas as pd
import json
import plotly 
import plotly.express as px

data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
data_df = pd.DataFrame(data)
data_df['InternetService'] = data_df['InternetService'].apply(lambda x: 'Yes' if x == 'DSL' or x == 'Fiber optic' else 'No')
data_df['OnlineSecurity'] = data_df['OnlineSecurity'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')
data_df['OnlineBackup'] = data_df['OnlineBackup'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')

data_df['Internet'] = int(0)
for i in range(len(data_df)):
    if data_df['InternetService'][i] == 'Yes' or data_df['OnlineSecurity'][i] == 'Yes' or data_df['OnlineBackup'][i] == 'Yes':
        data_df['Internet'][i] = 'Yes'
    else:
        data_df['Internet'][i] = 'No'


data_df['StreamingTV'] = data_df['StreamingTV'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')
data_df['StreamingMovies'] = data_df['StreamingMovies'].apply(lambda x: 'No' if x == 'No internet service' or x == 'No' else 'Yes')

data_df['Streaming'] = 0
for i in range(len(data_df)):
    if data_df['StreamingTV'][i] == 'Yes' or data_df['StreamingMovies'][i] == 'Yes':
        data_df['Streaming'][i] = 'Yes'
    else:
        data_df['Streaming'][i] = 'No'


data_df['TotalCharges'] = data_df['TotalCharges'].apply(lambda x: 0 if x == ' ' else x)
data_df['TotalCharges'] = data_df['TotalCharges'].astype(float)
data_df['MultipleLines'] = data_df['MultipleLines'].apply(lambda x: 'No' if x == 'No phone service' or x == 'No' else 'Yes')

data_df['total'] = 'all'


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

@app.route('/totalgraph') 
def totalgraph():
    fig1 = px.pie(data_df, values=data_df['Dependents'].value_counts(), names=['부양 가족 없음', '부양 가족 있음'], title='부양 가족 여부')
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    totalpieJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    charges_df = data_df.groupby(['total']).mean().reset_index()
    fig2 = px.bar(charges_df, x='total', y='TotalCharges', title='총 고객 평균 과금액')
    fig2.update_layout(yaxis_range=[0, 3550])
    totalchargesJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    fig3 = px.bar(charges_df, x='total', y='tenure', title='총 고객 평균 이용 기간(개월)')
    fig3.update_layout(yaxis_range=[0, 42])
    totaltenureJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    df = data_df.groupby(['PaymentMethod']).count().reset_index()
    fig4 = px.bar(df, x='PaymentMethod', y='Internet', title='총 고객 납부 방식')
    fig4.update_layout(yaxis_range=[0, 2370])
    totalmethodJSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    result = {"name" : "total",
                "data": {"pie": totalpieJSON, "charges" : totalchargesJSON, 
                "tenure": totaltenureJSON, "method" : totalmethodJSON}}
    result = json.dumps(result)
    return result

@app.route('/phonegraph') 
def phonegraph():
    fig1 = px.pie(data_df, values=data_df['MultipleLines'].value_counts(), names=['가입자', '미가입자'], title='MultiLine 가입 여부')
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    telepieJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    charges_df = data_df.groupby(['MultipleLines']).mean().reset_index()
    fig2 = px.bar(charges_df, x='MultipleLines', y='TotalCharges', title='MultiLine 가입 여부별 평균 과금액')
    fig2.update_layout(yaxis_range=[0, 3550])
    telechargesJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    fig3 = px.bar(charges_df, x='MultipleLines', y='tenure', title='MultiLine 가입 여부별 평균 이용 기간(개월)')
    fig3.update_layout(yaxis_range=[0, 42])
    teletenureJSON = json.dumps( fig3, cls=plotly.utils.PlotlyJSONEncoder)

    dfdf = data_df[data_df['MultipleLines'] == 'Yes']
    df = dfdf.groupby(['PaymentMethod']).count().reset_index()
    fig4 = px.bar(df, x='PaymentMethod', y='Internet', title='MultiLine 가입자 고객 납부 방식')
    fig4.update_layout(yaxis_range=[0, 2370])
    telemethodJSON = json.dumps( fig4, cls=plotly.utils.PlotlyJSONEncoder)

    result = {"name" : "phone",
                "data": {"pie": telepieJSON, "charges" : telechargesJSON, 
                "tenure": teletenureJSON, "method" : telemethodJSON}}
    result = json.dumps(result)
    return result

@app.route('/internetgraph') 
def internetgraph():
    fig1 = px.pie(data_df, values=data_df['Internet'].value_counts(), names=['가입자', '미가입자'], title='온라인 서비스 가입 여부')
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    onlinepieJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    charges_df = data_df.groupby(['Internet']).mean().reset_index()
    fig2 = px.bar(charges_df, x='Internet', y='TotalCharges', title='온라인 서비스 가입 여부별 평균 과금액')
    fig2.update_layout(yaxis_range=[0, 3550])
    onlinechargesJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    fig3 = px.bar(charges_df, x='Internet', y='tenure', title='온라인 서비스 가입 여부별 평균 이용 기간(개월)')
    fig3.update_layout(yaxis_range=[0, 42])
    onlinetenureJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    dfdf = data_df[data_df['Internet'] == 'Yes']
    df = dfdf.groupby(['PaymentMethod']).count().reset_index()
    fig4 = px.bar(df, x='PaymentMethod', y='Internet', title='온라인 서비스 가입자 고객 납부 방식')
    fig4.update_layout(yaxis_range=[0, 2370])
    onlinemethodJSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    fig5 = px.pie(data_df, values=data_df['Streaming'].value_counts(), names=['가입자', '미가입자'], title='스트리밍 서비스 가입 여부')
    fig5.update_traces(textposition="inside", textinfo="percent+label")
    streamingpieJSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    charges_df1 = data_df.groupby(['Streaming']).mean().reset_index()
    fig6 = px.bar(charges_df1, x='Streaming', y='TotalCharges', title='스트리밍 서비스 가입 여부별 평균 과금액')
    fig6.update_layout(yaxis_range=[0, 3550])
    streamingchargesJSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    fig7 = px.bar(charges_df1, x='Streaming', y='tenure', title='스트리밍 서비스 가입 여부별 평균 이용 기간(개월)')
    fig7.update_layout(yaxis_range=[0, 42])
    streamingtenureJSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)

    dfdf1 = data_df[data_df['Streaming'] == 'Yes']
    df1 = dfdf1.groupby(['PaymentMethod']).count().reset_index()
    fig8 = px.bar(df1, x='PaymentMethod', y='Streaming', title='스트리밍 서비스 가입자 고객 납부 방식')    
    fig8.update_layout(yaxis_range=[0, 2300])
    streamingmethodJSON = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)

    result = {"name" : "internet",
                "data": {"onlinepie": onlinepieJSON, "onlinecharges" : onlinechargesJSON, 
                "onlinetenure": onlinetenureJSON, "onlinemethod" : onlinemethodJSON,
                "streamingpie": streamingpieJSON, "streamingcharges" : streamingchargesJSON, 
                "streamingtenure": streamingtenureJSON, "streamingmethod" : streamingmethodJSON}
    }

    result = json.dumps(result)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)