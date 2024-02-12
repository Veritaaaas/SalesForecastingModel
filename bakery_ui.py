from flask import Flask, render_template, request, send_file
from new_model import predict_model

# creating the flask application
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return render_template('index.html')

# handles the submit HTTP request
@app.route('/submit', methods=['POST'])
def submit():
    article = request.form['bread']
    start_date = request.form['start-date']
    end_date = request.form['end-date']
    
    predict_model(article, start_date, end_date)
    
    return render_template('index.html')

# used for downloading the csv file
@app.route('/download')
def download():
    return send_file('forecast.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)