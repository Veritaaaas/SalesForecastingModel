from flask import Flask, render_template, request, send_from_directory, send_file
from statsmodels.tsa.statespace.sarimax import SARIMAX
from new_model import predict_model
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    article = request.form['bread']
    start_date = request.form['start-date']
    end_date = request.form['end-date']
    
    predict_model(article, start_date, end_date)
    
    return render_template('index.html')

@app.route('/download')
def download():
    return send_file('forecast.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)