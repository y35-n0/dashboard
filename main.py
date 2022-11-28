from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('root.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)