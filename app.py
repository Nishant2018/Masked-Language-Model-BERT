from flask import Flask, render_template, request
from model import BertModel
import os

app = Flask(__name__,static_folder='static')
device = "cpu"  # or "cuda" if you have a GPU available
# Get the absolute path to the model file
#model_path = os.path.join(os.path.dirname(__file__), 'Ml-Projects', 'Masked-Language-Model- BERT', 'BERT_model.pth')

bert_model = BertModel('BERT_model.pth', device)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_text = request.form['input_text']
        prediction = bert_model.predict(input_text)
        return render_template('index.html', input_text=input_text, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
